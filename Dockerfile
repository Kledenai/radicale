FROM python:3-alpine

# Version of Radicale (e.g. 3.0.x)
ARG VERSION=3.0.6
# Persistent storage for data (Mount it somewhere on the host!)
VOLUME /var/lib/radicale/collections
# Configuration data (Put the "config" file here!)
VOLUME /etc/radicale

RUN apk add --no-cache git

RUN /usr/local/bin/python3 -m pip install --upgrade pip

COPY radicale_ldap_auth /opt/radicale_ldap_auth
RUN  cd /opt/radicale_ldap_auth && python3 -m pip install .

# Copy config file to radicale folder config
COPY config /etc/radicale/config/config
# TCP port of Radicale (Publish it on a host interface!)

EXPOSE 5232
# Run Radicale (Configure it here or provide a "config" file!)
CMD ["radicale", "--config", "/etc/radicale/config/config"]

# Install dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev ca-certificates openssl
# Install Radicale
RUN pip install --no-cache-dir "Radicale[bcrypt] @ https://github.com/Kozea/Radicale/archive/${VERSION}.tar.gz"
# Remove build dependencies
RUN apk del gcc musl-dev libffi-dev
