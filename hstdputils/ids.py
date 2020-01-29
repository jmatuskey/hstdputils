
# ----------------------------------------------------------------------

# IPPPSSOOT   ---   dataset naming breakdown
#
# Denotes the instrument type:
# J - Advanced Camera for Surveys
# U - Wide Field / Planetary Camera 2
# V - High Speed Photometer
# W - Wide Field / Planetary Camera
# X - Faint Object Camera
# Y - Faint Object Spectrograph
# Z - Goddard High Resolution Spectrograph
# E - Reserved for engineering data
# F - Fine Guide Sensor (Astrometry)
# H-I,M - Reserved for additional instruments
# N - Near Infrared Camera Multi Object Spectrograph
# O - Space Telescope Imaging Spectrograph
# S - Reserved for engineering subset data
# T - Reserved for guide star position data
# PPP     Denotes the program ID, any combination of letters or numbers
# SS    Denotes the observation set ID, any combination of letters or numbers
# OO    Denotes the observation ID, any combination of letters or numbers
# T    Denotes the source of transmission:
# R - Real time (not tape recorded)
# T - Tape recorded
# M - Merged real time and tape recorded
# N - Retransmitted merged real time and tape recorded
# O - Retransmitted real time
# P - Retransmitted tape recorded
#

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
    return IPPPSSOOT_INSTR.get(ipppssoot.upper()[0])

def _get_instrument(instrument_or_ipppssoot):
    instrument_or_ipppssoot = instrument_or_ipppssoot.lower()
    if instrument_or_ipppssoot in INSTRUMENTS:
        return instrument_or_ipppssoot
    return get_instrument(instrument_or_ipppssoot)
    

# ----------------------------------------------------------------------

SUFFIX = {
    "acs" : [ "ASN", "RAW" ],
    "cos" : [ "ASN", "RAW", "EPC", "RAWACCUM", "RAWACCUM_A", "RAWACCUM_B", "RAWACQ", "RAWTAG", "RAWTAG_A", "RAWTAG_B"],
    "stis" : [ "ASN", "RAW", "EPC", "TAG",  "WAV" ], 
    "wfc3" : [ "ASN", "RAW" ],
}

DEFAULT_SUFFIX = ["RAW"]

def get_suffix(instrument_or_ipppssoot):
    """Given an IPPPSSOOT ID or instrument name,  return the corresponding
    suffixes which should be fetched for reprocessing using

    >>> get_suffix('cos')
    ['ASN','RAW', 'EPC', 'RAWACCUM', 'RAWACCUM_A', 'RAWACCUM_B', 'RAWACQ', 'RAWTAG', 'RAWTAG_A', 'RAWTAG_B']
    
    >>> get_suffix('LCYID1030')
    ['ASN', 'RAW', 'EPC', 'RAWACCUM', 'RAWACCUM_A', 'RAWACCUM_B', 'RAWACQ', 'RAWTAG', 'RAWTAG_A', 'RAWTAG_B']

    >>> get_suffix('STIS')
    ['ASN', 'RAW', 'EPC', 'TAG', 'WAV']

    >>> get_suffix('o8jhg2nnq')
    ['ASN', 'RAW', 'EPC', 'TAG', 'WAV']
    """
    instrument = _get_instrument(instrument_or_ipppssoot)
    return SUFFIX[instrument]

def get_bestrefs_suffix(instrument_or_ipppssoot):
    """Return the tuple of file suffixes bestrefs should process suitable for use with .endswith().
    >>> get_bestrefs_suffix("acs")
    >>> get_bestrefs_suffix("cos")
    >>> get_bestrefs_suffix("stis")
    >>> get_bestrefs_suffix("wfc3")
    """
    suffix = get_suffix(instrument_or_ipppssoot)
    filesuffix = tuple(
        [ "_" + s.lower() + ".fits" for s in suffix
          if "RAW" in ])
    return filesuffix

# ----------------------------------------------------------------------

EXECUTABLE = {
    "acs" : "calacs.e",
    "cos" : "calcos",
    "stis" : "cs0.e -tv",
    "wfc3" : "calwf3.e",
    }

def  get_executable(instrument_or_ipppssoot):
    """
    >>> get_executable('acs')
    'calacs.e'

    >>> get_executable('O8JHG2NNQ')
    'cs0.e -tv'
    """
    instrument = _get_instrument(instrument_or_ipppssoot)
    return EXECUTABLE[instrument]

# ----------------------------------------------------------------------

def test():
    import doctest
    from hstdputils import ids
    return doctest.testmod(ids)

if __name__ == "__main__":
    print(test())

