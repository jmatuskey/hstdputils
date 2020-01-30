import sys
import datetime
from collections import namedtuple

from hstdputils import process

# ----------------------------------------------------------------------

def get_batch_name(name):
    when = datetime.datetime.now().isoformat()
    when = when.replace(":","-")
    when = when.replace(".","-")
    return name + "-" + when[:-7]   # drop subseconds

IdInfo = namedtuple("IdInfo", ["ipppssoot", "instrument", "executable", "cpus", "memory", "max_seconds"])

JOB_INFO = {
    "acs" : ("acs", "hstdp-process", 4, 2*1024, 60*60*4),
    "cos" : ("cos", "hstdp-process", 1, 1*1024, 60*20),
    "stis" : ("stis", "hstdp-process", 1, 1*1024, 60*20),
    "wfc3" : ("wfc3", "hstdp-process", 4, 2*1024, 60*60*4),
    }

def id_info(ipppssoot):
    """Given an HST IPPPSSOOT ID,  return information used to schedule it as a batch job.
    Returns:  (ipppssoot, instrument, executable, cpus, memory, max_seconds)
    """
    instr = process.get_instrument(ipppssoot)
    return IdInfo(*(ipppssoot,)+JOB_INFO[instr])

def planner(output_bucket, batch_prefix, ipppssoots):
    batch_name = get_batch_name(batch_prefix)
    for ipppssoot in ipppssoots:
        if process.IPPPSSOOT_RE.match(ipppssoot.upper()):
            print(plan(output_bucket, batch_name, ipppssoot))
        else:
            print(ipppssoot, file=sys.stderr)

def plan(output_bucket, batch_prefix, ipppssoot):
    prefix = batch_prefix + "/" + ipppssoot
    plan = (output_bucket, prefix,) + id_info(ipppssoot)
    return plan

# ----------------------------------------------------------------------

def test():
    import doctest
    from hstdputils import planner
    return doctest.testmod(planner)

if __name__ == "__main__":
    if sys.argv[0] == "test":
        print(test())
    else:
        output_bucket = sys.argv[1]
        batch_prefix = sys.argv[2]
        ipppssoots = sys.argv[3:]
        planner(output_bucket, batch_prefix, ipppssoots)
