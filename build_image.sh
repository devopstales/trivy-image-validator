#!/bin/sh
VERSION=$(curl --silent "https://api.github.com/repos/aquasecurity/trivy/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/' | sed 's/^.\{1\}//')
wget -q -O /tmp/trivy.tar.gz https://github.com/aquasecurity/trivy/releases/download/v"$VERSION"/trivy_"$VERSION"_Linux-64bit.tar.gz
tar -C /tmp -xf /tmp/trivy.tar.gz
cp /tmp/trivy deploy/docker
cp trivy-scanner.py deploy/docker
cp requirements.txt deploy/docker
cp certs/server.pem deploy/docker/
docker build -t $1 \
  deploy/docker
rm -f deploy/docker/trivy-scanner.py
rm -f deploy/docker/trivy
rm -f deploy/docker/requirements.txt
rm -f certs/server.pem