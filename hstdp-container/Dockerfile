# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.

# DATB's HST CAL code build for the pipeline
FROM astroconda/datb-tc-pipeline:hstdp-snapshot

LABEL maintainer="jmiller@stsci.edu" \
      vendor="Space Telescope Science Institute"

# Environment variables
ENV MKL_THREADING_LAYER="GNU"

USER root

# RUN yum update  -y

RUN yum install -y curl rsync time

# Install hstdp conda environment
# RUN conda create -n hstdp --file http://ssb.stsci.edu/releases/hstdp/2019.5/latest-linux

RUN pip install awscli boto3
RUN pip install jupyterlab
RUN pip install --upgrade git+https://github.com/jaytmiller/hstdputils.git

WORKDIR /home/developer
USER developer

CMD ["/bin/bash"]
