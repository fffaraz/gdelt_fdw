FROM postgres:11.2
RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
build-essential ca-certificates git postgresql-server-dev-${PG_MAJOR} python3-dev python3-pip python3-setuptools && \
alias python=python3 && \
ln -s $(which python3) /usr/bin/python && \
ln -s $(which python3) /usr/local/bin/python && \
ls -l /usr/bin/python* && \
ls -l /usr/local/bin/python* && \
git clone git://github.com/Kozea/Multicorn.git && \
cd Multicorn && \
make && make install && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
