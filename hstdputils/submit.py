import sys

import boto3

# QUEUE = "arn:aws:batch:us-east-1:162808325377:job-queue/hstdp-batch-queue"
# JOB_DEFINITION = "arn:aws:batch:us-east-1:162808325377:job-definition/hstdp-ipppssoot-job:10"

QUEUE = "hstdp-batch-queue"
JOB_DEFINITION = "hstdp-ipppssoot-job"

def submit_job(plan):
    """Given a job description tuple `plan` from the planner,  submit a job to AWS batch."""
    bucket, prefix, ipppssoot, instrument, command, vcpus, memory, seconds = plan
    client = boto3.client("batch")
    job = {
        "jobName": prefix.replace("/","-"),
        "jobQueue": QUEUE,
        "jobDefinition": JOB_DEFINITION,
        "containerOverrides": {
            # "image": DOCKER_IMAGE,
            "vcpus": vcpus,
            "memory": memory,
            "command": [
                command,
                bucket,
                prefix,
                ipppssoot
            ],
        },
        "timeout": {
            "attemptDurationSeconds": seconds,
        },
    }
    return client.submit_job(**job)


def main(plan_file):
    """Given a file `plan_file` defining job plan tuples one-per-line,  
    submit each job and output the plan and submission response to stdout.
    """
    with open(plan_file) as f:
        for line in f.readlines():
            job_plan = eval(line)
            print("----", job_plan)
            print(submit_job(job_plan))

if __name__ == "__main__":
    main(sys.argv[1])
