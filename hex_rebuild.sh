#!/usr/bin/env bash

# rebuild the hex into a zip binary 
xxd -r -p dns_exfil_output.hex > secret_documents.zip
#  unzip the file
unzip secret_documents.zip
