FROM postgres:10
ENV LC_CTYPE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
build-essential ca-certificates git postgresql-server-dev-${PG_MAJOR} python-dev python-setuptools && \
locale-gen en_US en_US.UTF-8 && \
dpkg-reconfigure locales && \
git clone git://github.com/Kozea/Multicorn.git && \
cd Multicorn && \
make && make install && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
