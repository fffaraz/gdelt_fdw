FROM postgres:10
RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
build-essential ca-certificates git postgresql-server-dev-${PG_MAJOR} python-dev && \
git clone git://github.com/Kozea/Multicorn.git && \
cd Multicorn && \
make && make install && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
