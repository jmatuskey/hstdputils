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
processing for HST IPPPSSOOT's, job planning, and Batch Job
submission.  Acts as a replacement for OWL CAL code wrapper scripts.

#### Core execution in container

```
python -m hstdputils.process <output_bucket>  <batch_name>  <ipppssoots....>
```

hstdputils.process obtains data and references for the specified ipppssoot's,
processes appropriately for each ippssoot,  and copies output files to an
S3 target based on output_bucket, batch_name, and the copied filename.  If
output_bucket ==  "none" then no S3 results saving is performed.

As currently implemented the process routine supports multiple ipppsoots in
the same batch and will put them all in the same output S3 target directory.

#### Job planning based on IPPPSSOOT's to determine RAM and CPU requirements

```
python -m hstdputils.plan <output_bucket>  <batch_name> < ipppssoots...> >plan.out
```

The planner is intended to map IPPPSSOOT's onto appropriate resources and
executables.   Currently it is stubbed at the instrument level to determine
resource requirements but in principle could determine requirements based on
a database and individual IPPPSSOOT's.  This resource determination is critical
to the operation of AWS Batch and the type and number of worker nodes which
will be automatically created.

## scripts

Glue scripts which make it easy to initialize different environments
and execute HST processing in the container.

Provides a clean Docker command line with additional functionality
like combined log capture and metrics collection, exported to S3.

#### Docker run command for AWS

```
hstdp-process  <output-bucket>  <batch-name>   <ipppssoots...>
```

This command configures CRDS for S3, captures CPU and memory metrics,
captures a combined log, and runs python -m hstdputils.process
mentioned above.

#### Run command for laptop hstdputils pip installs;  CAL code not included

```
hstdputils-remote-process  <ipppssoot's...>
```

For offsite laptop use.  Downloads required files from STScI CRDS.

```
hstdputils-onsite-process  <ipppssoot's...>
```

For onsite use.  Uses onsite serverless configuration and /grp/crds/cache.

```
hstdputils-docker-run-container <command...>
```

Just run whatever command is given,  do not assume hstdp-process.

```
hstdputils-docker-run-pipeline <output-bucket> <batch-name> <ipppssoot's...>
```

## batch

Currently just captured JSON configs of AWS Batch resources created
with AWS console wizards.

This package was originally prototyped to target AWS batch but elements
are equally applicable to other container execution approaches and/or
more native approaches such as HTCondor.

#### Command to submit plan to Batch

This command is the only direct tie to Batch:

```
python -m hstdputils.submit  plan.out
```

For each job listed in `plan.out`,  hstputils.submit queues one Batch
job.   This command is e.g. run on the Batch control node, input Lambda,
etc.

Potentially other versions of submit could submit plans in other workflow
environments,  wherever it's useful to know CPU and memory requirements in
advance.

