import os
import sys
import glob
import re

from drizzlepac.hlautils.astroquery_utils import retrieve_observation

from crds.bestrefs import bestrefs

from . import s3
from . import log

# -----------------------------------------------------------------------------

IPPPSSOOT_RE = re.compile(r"^[IJLO][A-Z0-9]{8,8}$")

IPPPSSOOT_INSTR = {
    "J" : "acs",
    "U" : "wfpc2",
    "V" : "hsp",
    "W" : "wfpc",
    "X" : "foc",
    "Y" : "fos",
    "Z" : "hrs",
    "E" : "eng",
    "F" : "fgs",
    "I" : "wfc3",
    "N" : "nicmos",
    "O" : "stis",
    "L" : "cos",
}

INSTRUMENTS = set(IPPPSSOOT_INSTR.values())

def get_instrument(ipppssoot):
    """Given an IPPPSSOOT ID, return the corresponding instrument.

    >>> get_instrument("JBW2BGNKQ")
    'acs'
    
    >>> get_instrument("LCYID1030")
    'cos'

    >>> get_instrument("O8JHG2NNQ")
    'stis'

    >>> get_instrument("IDDE02XSQ")
    'wfc3'
    """
    if ipppssoot.lower() in INSTRUMENTS:
        return ipppssoot.lower()
    else:
        return IPPPSSOOT_INSTR.get(ipppssoot.upper()[0])

# -----------------------------------------------------------------------------

class InstrumentManager:
    name = None # abstract class
    suffixes = None

    def divider(self, *args, dash="-"):
        msg = " ".join([str(a) for a in args])
        dashes = (100-len(msg)-2-5)
        log.info("-"*5, msg, "-"*dashes)
        
    def dowload(self, ipppssoot):
        self.divider("Retrieving files for:", ipppssoot)
        files = retrieve_observation(ipppssoot, suffix=self.suffixes)
        self.divider("Downioad complete for:", ipppssoot)
        return files
        
    def assign_bestrefs(self, ipppssoot, files):
        self.divider("Computing bestrefs for:", ipppssoot, files)
        bestrefs_files = self.raw_files(files)
        bestrefs.assign_bestrefs(bestrefs_files, sync_references=True)
        self.divider("Bestrefs complete for:", ipppssoot)
        return bestrefs_files

    def run(self, *args):
        self.divider("Running:", *args)
        cmd = " ".join(args)
        err = os.system(cmd)
        if err:
            log.error("Command:", repr(cmd), "exited with non-zero error status:", err)
            sys.exit(1) # should be 0-127,  higher err val's like 512 are truncated to 0 by shells

    def process(self, ipppssoot, files):
        assoc = [f for f in files if f.endswith("_asn.fits")]
        if assoc:
            self.run(self.stage1, *assoc)
            if self.stage2:
                self.run(self.stage2, *assoc)
        else:
            self.run(self.stage1, *self.raw_files(files))
            
    def raw_files(self, files):
        return [f for f in files if "_raw" in f]

    def output_files(self, outputs, output_bucket=None, prefix=None):
        self.divider("Saving outputs:", outputs)
        if output_bucket:
            for filename in outputs:
                log.info("Saving:", filename)
                s3.upload_filename(filename, output_bucket, prefix=prefix)

# -----------------------------------------------------------------------------

class AcsManager(InstrumentManager):
    name = "acs"
    suffixes = ["ASN", "RAW"]
    stage1 = "calacs.e"
    stage2 = "runastrodriz"
    
class Wfc3Manager(InstrumentManager):
    name = "wfc3"
    suffixes = ["ASN", "RAW"]
    stage1 = "calwf3.e"
    stage2 = "runastrodriz"

# ............................................................................
    
class CosManager(InstrumentManager):
    name = "cos"
    suffixes = ["ASN", "RAW", "EPC", "RAWACCUM", "RAWACCUM_A", "RAWACCUM_B", "RAWACQ", "RAWTAG", "RAWTAG_A", "RAWTAG_B"]
    stage1 = "calcos"
    stage2 = None

    def raw_files(self, files):
        return super(CosManager, self).raw_files(files)[:1]   # return only first file
    
# ............................................................................
    
class StisManager(InstrumentManager):
    name = "stis"
    suffixes = ["ASN", "RAW", "EPC", "TAG",  "WAV"]
    stage1 = "cs0.e -tv"
    stage2 = None

    def process(self, ipppssoot, files):
        raw = [ f for f in files if f.endswith("_raw.fits")]
        wav = [ f for f in files if f.endswith("_wav.fits")]
        if raw:
            self.run(self.stage1, *raw)
        else:
            self.run(self.stage1, *wav)

    def raw_files(self, files):
        return [f for f in files if f.endswith(('_raw.fits','_wav.fits','_tag.fits'))]

# ............................................................................
    
MANAGERS = {
    "acs" : AcsManager(),
    "cos" : CosManager(),
    "stis" : StisManager(),
    "wfc3" : Wfc3Manager(),
    }

def get_instrument_manager(ipppssoot):
    instrument = get_instrument(ipppssoot)
    manager = MANAGERS[instrument]
    manager.divider("Started processing for", instrument, ":", ipppssoot)
    return manager

# -----------------------------------------------------------------------------

def process(ipppssoot, output_bucket=None, prefix=None):
    """Given a `prefix` a dataset `ipppssoot` ID and an S3 `output_bucket`,
    process the dataset and upload output products to the `output_bucket` with
    the given `prefix`.

    Nominally `prefix` identifies a job or batch of files dumped into an 
    otherwise immense bucket.
    """
    manager = get_instrument_manager(ipppssoot)

    files = manager.dowload(ipppssoot)

    manager.assign_bestrefs(ipppssoot, files)
    
    manager.process(ipppssoot, files)
    
    all = glob.glob("*.fits")
    outputs = list(set(all) - set(files))

    manager.output_files(outputs, output_bucket, prefix)
    
    return outputs

# -----------------------------------------------------------------------------

def process_ipppssoots(ipppssoots, output_bucket=None, prefix=None):
    for ipppssoot in ipppssoots:
        process(ipppssoot, output_bucket, prefix)

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    output_bucket = sys.argv[1]
    prefix = sys.argv[2]
    ipppssoots = sys.argv[3:]
    if output_bucket.lower() == "none":
        output_bucket = None
    if prefix.lower() == "none":
        prefix = None
    process_ipppssoots(ipppssoots, output_bucket, prefix)
