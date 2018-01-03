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
        default-jre && \
    apt-get clean

# Point $TEXMFHOME to the container's lsst-texmf. This environment variable
# exists for container runs by a user.
ENV TEXMFHOME "/texmf"

# Add lsst-texmf's bin/ directory to the path
ENV PATH="/lsst-texmf-bin:${PATH}"

RUN mkdir $TEXMFHOME && mkdir /lsst-texmf-bin

# Contents of the lsst-texmf Git repo's texmf/ directory copied to container's
# $TEXMFHOME directory.
COPY texmf $TEXMFHOME/

# Copy contents of lsst-texmf's bin directory to the image
COPY bin /lsst-texmf-bin/

CMD ["/bin/echo", "See https://lsst-texmf.lsst.io/docker.html for usage."]
