import datetime
from collections import namedtuple

from hstdputils import ids

# ----------------------------------------------------------------------

def get_batch_name(name):
    when = datetime.datetime.now().isoformat()
    when = when.replace(":","-")
    when = when.replace(".","-")
    return name + "-" + when

IdInfo = namedtuple("IdInfo", ["ipppssoot", "instrument", "executable", "cpus", "memory", "max_seconds"])

def id_info(ipppssoot):
    """Given an HST IPPPSSOOT ID,  return information used to schedule it as a batch job.

    >>> id_info("J8EO02010")
    IdInfo(ipppssoot='J8EO02010', instrument='acs', executable='calacs.e', cpus='1', memory='8196', max_seconds='3600')

    Returns:  (ipppssoot, instrument, executable, cpus, memory, max_seconds)
    """
    instr = ids.get_instrument(ipppssoot)
    program = ids.get_executable(instr)
    memory = 8196  # megabytes
    cpus = 1
    seconds = 60*60
    return IdInfo(ipppssoot, instr, program,  str(cpus),  str(memory),  str(seconds))

# ----------------------------------------------------------------------

def test():
    import doctest
    from hstdputils import planner
    return doctest.testmod(planner)

if __name__ == "__main__":
    if sys.argv[0] == "test":
        print(test())
    else:
        plan(sys.argv[1:])
