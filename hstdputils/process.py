import os
import sys
import glob

from . import download
from . import bestrefs
from . import s3
from . import ids
from . import planner

# -----------------------------------------------------------------------------

def process(ipppssoot, output_bucket=None, prefix=None):
    """Given a `prefix` a dataset `ipppssoot` ID and an S3 `output_bucket`,
    process the dataset and upload output products to the `output_bucket` with
    the given `prefix`.

    Nominally `prefix` identifies a job or batch of files dumped into an 
    otherwise immense bucket.
    """
    files = download.download(ipppssoot)

    info = planner.id_info(ipppssoot)

    for filename in planner.process_files(info, files):
        bestrefs.assign_bestrefs(filename)
        err = os.system(info.executable + " " + filename)

    all = glob.glob("*.fits")
    outputs = list(set(all) - set(files))
    
    output_files(outputs, output_bucket, prefix)
    
    return outputs

def process_ipppssoots(ipppssoots, output_bucket=None, prefix=None):
    for ipppssoot in ipppssoots:
        process(ipppssoot, output_bucket, prefix)

# -----------------------------------------------------------------------------

def output_files(files, output_bucket=None, prefix=None):
    if output_bucket:
        for filename in files:
            s3.upload_filename(filename, output_bucket, prefix=prefix)

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    output_bucket = sys.argv[1]
    prefix = sys.argv[2]
    ipppssoots = sys.argv[3:]
    process_ipppssoots(ipppssoots, output_bucket, prefix)
