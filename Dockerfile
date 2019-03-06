FROM postgres:10
RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
build-essential ca-certificates curl git postgresql-server-dev-${PG_MAJOR} python-dev python-setuptools wget && \
git clone git://github.com/fffaraz/Multicorn.git && \
cd Multicorn && \
make && make install && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
COPY fdw /fdw
RUN cd /fdw && python setup.py install
