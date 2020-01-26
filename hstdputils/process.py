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
    outputs = set(all) - set(files)
    if output_bucket:
        for filename in outputs:
            s3.upload_filename(filename, output_bucket, prefix=prefix)
    return outputs

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    process(*sys.argv[1:])
