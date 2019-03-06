FROM php:apache
RUN \
set -eux && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y \
zlib1g-dev libzip-dev && \
docker-php-ext-install zip && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
