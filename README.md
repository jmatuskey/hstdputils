# calcloud

This package contains utilities used to support processing for HST
CALCLOUD batch jobs and related tasks.

There are four broad areas of the repo:

## hstdp-container

Dockerfile and scripts related to building a Docker container with HST
CAL pipeline processing executables.  This is largely based on DATB's
Docker image for HST CAL augmented for AWS and these utilities.
		   
## hstdputils

Auxilliary package which is installed both on Batch control nodes (or
perhaps Lambdas) and within the hstdp-container.  Provides generalized
processing for HST IPPPSSOOT's, Batch planning, and Batch Job
submission.  Acts as a replacement for OWL CAL code wrapper scripts.

## scripts

Glue scripts which make it easy to initialize different environments
and execute HST processing in the container.  Provides a clean Docker
run command line with additional functionality like combined log
capture and metrics collection, exported to S3.

## batch

Currently just captured JSON configs of AWS Batch resources created
with AWS console wizards.

This package was originally prototyped to target AWS batch but elements
are equally applicable to other container execution approaches and/or
more native approaches such as HTCondor.

