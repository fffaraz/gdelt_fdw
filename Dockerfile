FROM postgres:11.2
RUN \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y build-essential ca-certificates postgresql-server-dev-${PG_MAJOR} python-setuptools && \
easy_install pgxnclient && \
pgxn install multicorn && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
