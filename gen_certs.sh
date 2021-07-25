#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# CREATE THE PRIVATE KEY FOR OUR CUSTOM CA
openssl genrsa -out certs/rootCA.key 4096 -days 36500

# GENERATE A CA CERT WITH THE PRIVATE KEY
openssl req -new -x509 -nodes -key certs/rootCA.key -sha256 -out certs/rootCA.crt -subj "/CN=Admission Controller Webhook" -days 36500

# CREATE THE PRIVATE KEY FOR OUR SERVER
openssl genrsa -out certs/tls.key 2048 -days 36500

# CREATE A CSR FROM THE CONFIGURATION FILE AND OUR PRIVATE KEY
openssl req -new -sha256 -key certs/tls.key -out certs/tls.csr -config certs/server_config.txt

# CREATE THE CERT SIGNING THE CSR WITH THE CA CREATED BEFORE
openssl x509 -req -in certs/tls.csr -CA certs/rootCA.crt -CAkey certs/rootCA.key -CAcreateserial -out certs/tls.crt -sha256 -extfile certs/server_config.txt -extensions req_ext -days 36500

# Create .pem versions
cat certs/tls.crt certs/tls.key > certs/tls.pem

# INJECT CA IN THE WEBHOOK CONFIGURATION
export CA_BUNDLE=$(cat certs/rootCA.crt | base64 | tr -d '\n')
rm -f deploy/kubernetes/vwc.yaml
cat deploy/kubernetes/template/_vwc.yaml | envsubst > deploy/kubernetes/vwc.yaml
