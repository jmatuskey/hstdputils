from crds.bestrefs import bestrefs

def assign_bestrefs(file, download=True):
    """Set the FITS header keywords of `file` to the corresponding best reference file paths.
    
    If `download` is True,  sync the best references into the CRDS cache,  skipping any repeat downloads.

    Returns whatever crds.bestrefs.assign_bestrefs does.   Presumably a count of errors.
    """
    return bestrefs.assign_bestrefs([file], sync_references=download) # , verbosity=50)

