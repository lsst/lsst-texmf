# Dockerized lsst-texmf
#
# https://github.com/lsst/lsst-texmf
#
# Base image: https://github.com/lsst-sqre/lsst-texlive

FROM lsstsqre/lsst-texlive:latest
MAINTAINER LSST SQuaRE <sqre-admin@lists.lsst.org>

# Point $TEXMFHOME to the container's lsst-texmf. This environment variable
# exists for container runs by a user.
ENV TEXMFHOME "/texmf"

# Create $TEXMFHOME directory in the container
RUN mkdir $TEXMFHOME

# Contents of the lsst-texmf Git repo's texmf/ directory copied to container's
# $TEXMFHOME directory.
COPY texmf $TEXMFHOME/

CMD ["/bin/echo", "See https://lsst-texmf.lsst.io/docker.html for usage."]
