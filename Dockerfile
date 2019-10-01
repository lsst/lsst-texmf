# Dockerized lsst-texmf
#
# https://github.com/lsst/lsst-texmf
#
# Base image: https://github.com/lsst-sqre/lsst-texlive

FROM lsstsqre/lsst-texlive:latest
MAINTAINER LSST SQuaRE <sqre-admin@lists.lsst.org>

# Additional dependencies for lsst-texmf (acronyms.csh)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        csh \
        python3-pip \
        python3-setuptools \ 
        default-jre && \
    apt-get clean

# Create a directory the lsst-texmf installation
RUN mkdir lsst-texmf

# Point $TEXMFHOME to the container's lsst-texmf. This environment variable
# exists for container runs by a user.
ENV TEXMFHOME "/lsst-texmf/texmf"

# Add lsst-texmf's bin/ directory to the path
ENV PATH="/lsst-texmf/bin:${PATH}"

# Copy lsst-texmf repo in /lsst-texmf/
COPY . /lsst-texmf

# Python dependencies
RUN pip3 install -r /lsst-texmf/requirements.txt

CMD ["/bin/echo", "See https://lsst-texmf.lsst.io/docker.html for usage."]
