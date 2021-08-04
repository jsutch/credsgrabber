# coding: utf-8
"""
You'll need to tailor this to your own file output, but the main steps are simple:
    - determine what lookups are relevant
    - pull the lookup chunk and remove the domain
    - patch that into an output hexfile, in order
    - profit!
"""
import os

targetdomain='mydomain.net'

# import the named.log and remove EOLs
rawlog = open('named.log','r').readlines()
logs = [x.strip('\n') for x in rawlog]
# build an array of names looked up that match the target domain
lookups = [x.split(' ')[9]  for x in logs if targetdomain in x]
# scrub ordinary names. This can be tricky since a hex file might have an ending line < the usual 60chars.
# test your smallest xfer'd hex line in case len() is not the right test for correctness
ignorehosts = [x for x in set(lookups) if len(x) < 20]

# put it all together
# we're using a dict to track potential multiples and a list for the final output
# since dict doesn't guarantee order. This could be a single store with an OrderedDict.
final, stash = [], {}
for x in lookups:
    if x not in stash and line not in ignorehosts:
        line = x.split('.')[0]
        stash[x] = 1
        final.append(line)


# write out the file
with open('dns_exfil_output.hex','w') as f:
     for l in final:
         line = l + '\n'
         f.write(line)
f.close()
