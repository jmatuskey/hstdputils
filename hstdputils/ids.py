
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
    "cos" : [ "RAW", "RAWACCUM", "RAWACCUM_A", "RAWACCUM_B", "RAWACQ", "RAWTAG", "RAWTAG_A", "RAWTAG_B"],
    }

DEFAULT_SUFFIX = ["ASN", "RAW"]

def get_suffix(instrument_or_ipppssoot):
    """Given an IPPPSSOOT ID or instrument name,  return the corresponding
    suffixes which should be fetched for reprocessing using

    >>> get_suffix('cos')
    ['RAW', 'RAWACCUM', 'RAWACCUM_A', 'RAWACCUM_B', 'RAWACQ', 'RAWTAG', 'RAWTAG_A', 'RAWTAG_B']
    
    >>> get_suffix('LCYID1030')
    ['RAW', 'RAWACCUM', 'RAWACCUM_A', 'RAWACCUM_B', 'RAWACQ', 'RAWTAG', 'RAWTAG_A', 'RAWTAG_B']

    >>> get_suffix('STIS')
    ['ASN', 'RAW']

    >>> get_suffix('o8jhg2nnq')
    ['ASN', 'RAW']
    """
    instrument = _get_instrument(instrument_or_ipppssoot)
    return SUFFIX.get(instrument, DEFAULT_SUFFIX)

def get_file_suffix(instrument_or_ipppssoot):
    suffix = get_suffix(instrument_or_ipppssoot)
    filesuffix = tuple([ "_" + s.lower() + ".fits" for s in suffix ])
    return filesuffix

# ----------------------------------------------------------------------

EXECUTABLE = {
    "acs" : "calacs.e",
    "cos" : "calcos",
    "stis" : "python -m stistools.calstis",
    "wfc3" : "calwf3.e",
    }

def  get_executable(instrument_or_ipppssoot):
    """
    >>> get_executable('acs')
    'calacs.e'

    >>> get_executable('O8JHG2NNQ')
    'calstis.e'
    """
    instrument = _get_instrument(instrument_or_ipppssoot)
    return EXECUTABLE.get(instrument, "cal" + instrument + ".e")    

# ----------------------------------------------------------------------

def test():
    import doctest
    from hstdputils import ids
    return doctest.testmod(ids)

if __name__ == "__main__":
    print(test())

