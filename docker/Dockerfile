FROM postgres:12.1

ENV PGUSER postgres
ENV PYTHON_OVERRIDE python3.7
ENV LC_ALL C.UTF-8

RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
build-essential ca-certificates clang curl git \
postgresql-server-dev-${PG_MAJOR} \
postgresql-client-${PG_MAJOR} \
libpython3.7-dev python3.7-dev python3-setuptools wget && \
git clone git://github.com/Kozea/Multicorn.git && \
cd Multicorn && \
make -j $(nproc) && make install && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

COPY fdw /fdw

RUN cd /fdw && python3 setup.py install
