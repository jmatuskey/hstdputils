import os, os.path

import boto3

# -------------------------------------------------------------

def upload_filename(filename, bucket, objectname=None, prefix=None):
    if objectname  is None:
        objectname = object_name(filename, prefix)
    s3 = boto3.client('s3')
    with open(filename, "rb") as f: 
        s3.upload_fileobj(f, bucket, objectname)

def download_filename(filename, bucket, objectname=None, prefix=None):
    if objectname  is None:
        objectname = object_name(filename, prefix)
    s3 = boto3.client('s3')
    with open(filename, "wb+") as f:
        s3.download_fileobj(bucket, objectname, f)
    
# -------------------------------------------------------------

def object_name(filename, prefix=None):
    object_name = os.path.basename(filename).split(".")[0]
    if prefix is not None:
        object_name = prefix + object_name
    return object_name

