from drizzlepac.hlautils.astroquery_utils import retrieve_observation

from hstdputils import ids

def download(ipppssoot): 
    return retrieve_observation(ipppssoot, suffix=ids.get_suffix(ipppssoot))



