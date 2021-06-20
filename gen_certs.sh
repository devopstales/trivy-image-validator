#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# CREATE THE PRIVATE KEY FOR OUR CUSTOM CA
openssl genrsa -out certs/ca.key 4096

# GENERATE A CA CERT WITH THE PRIVATE KEY
openssl req -new -x509 -nodes -key certs/ca.key -sha256 -out certs/ca.crt -subj "/CN=Admission Controller Webhook"

# CREATE THE PRIVATE KEY FOR OUR SERVER
openssl genrsa -out certs/server.key 2048

# CREATE A CSR FROM THE CONFIGURATION FILE AND OUR PRIVATE KEY
openssl req -new -sha256 -key certs/server.key -out certs/server.csr -config certs/server_config.txt

# CREATE THE CERT SIGNING THE CSR WITH THE CA CREATED BEFORE
openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/server.crt -sha256 -extfile certs/server_config.txt -extensions req_ext

# Create .pem versions
cat certs/server.crt certs/server.key > certs/server.pem

# INJECT CA IN THE WEBHOOK CONFIGURATION
export CA_BUNDLE=$(cat certs/ca.crt | base64 | tr -d '\n')
rm -f deploy/kubernetes/vwc.yaml
cat deploy/kubernetes/template/_vwc.yaml | envsubst > deploy/kubernetes/vwc.yaml