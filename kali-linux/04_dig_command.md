# DIG

Domain Information Groper (dig) command line tool is used for performing DNS querying.

Check installation/version:
```
$ dig -v
DiG 9.11.16-2-Debian
```

Example:

```shell
$ dig linux.org

; <<>> DiG 9.11.16-2-Debian <<>> linux.org
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19330
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 8192
;; QUESTION SECTION:
;linux.org.                     IN      A

;; ANSWER SECTION:
linux.org.              300     IN      A       104.21.31.121
linux.org.              300     IN      A       172.67.176.128

;; Query time: 50 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Sep 07 01:21:31 CDT 2021
;; MSG SIZE  rcvd: 70

```

> Tip: get a short answer to your query by using the `+short` option:
```shell
$ dig linux.org +short
172.67.176.128
104.21.31.121
```

# Exclude/Include Output

### Exclude First Two Lines
First line outputs the version and the queried domain name. -The second line shows the global options.
To exclude these to lines, use the `+nocmd` option.

### Exclude Header Section
The header shows the opcode (action performed by dig) and the status of the action. `NOERROR` status means that the requested authority served the query without any errors.

Exclude this section by  using the `+nocomments` option, which also disables some other section's headers.

### Exclude the OPT PSEUDOSECTION
To exclude this section use the `+noedns` option.

### Exclude Question Section
The "QUESTION" section shows the query. Exclude this section by using the `+noquestion` option.

### Exclude Answer Section
The "ANSWER" section displays an answer to our question. Usually, it is not wanted to turn off the answer, but to exclude this from the output use the `+noanswer` option.

### Exclude Statistics
The last section of the output includes statistics about the query:
```
;; Query time: 58 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Fri Oct 12 11:46:46 CEST 2018
;; MSG SIZE  rcvd: 212
```
Exclude this statistic section fromt he output with the `+nostats` option.


## Print Answers

## Get Short Answer
Get a short version of the answers from the `dig` query by using the `+short` option.

```shell
$ dig linux.org +short
172.67.176.128
104.21.31.121
```

## Get Detailed Answer
Turn off all the results with the `+noall` option and ten turn on the answer section with the `+answer` option.
```shell
$ dig linux.org +noall +answer
linux.org.              300     IN      A       104.21.31.121
linux.org.              300     IN      A       172.67.176.128
```

<hr>

## Query Specific Name Server
`dig` by default usese the servers listed in `/etc/reolv.conf` file.

Use the `@` symbol folled by the name server ip address or hostname to specify a name server against which the query will be executed.

Example: query the Google name server (8.8.8.8) for the `linux.org` domain.
```shell
$ dig linux.org @8.8.8.8

; <<>> DiG 9.11.16-2-Debian <<>> linux.org @8.8.8.8
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20268
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;linux.org.                     IN      A

;; ANSWER SECTION:
linux.org.              300     IN      A       104.21.31.121
linux.org.              300     IN      A       172.67.176.128

;; Query time: 47 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Tue Sep 07 01:27:29 CDT 2021
;; MSG SIZE  rcvd: 70
```

<hr>

## Query Record Type
1. Query **A** records - get list of all the address(es) for a domain name, use the `a` option:
    ```shell
    $ dig +nocmd google.com a +noall +answer
    google.com.             244     IN      A       172.217.14.174
    ```
2. Query **CNAME** records - find the alias domain name, use the `cname` option:
	```shell
	$dig +nocmd mail.google.com cname +noall +answer
	mail.google.com.        552614  IN      CNAME   googlemail.l.google.com.
	```
3. Query **TXT** records - retrieve all the TXT records for a specific domain
	```shell	
	$ dig +nocmd google.com txt +noall +answer
	google.com.             3600    IN      TXT     "docusign=1b0a6754-49b1-4db5-8540-d2c12664b289"
	google.com.             3600    IN      TXT     "facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95"
	google.com.             3600    IN      TXT     "MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB"
	google.com.             3600    IN      TXT     "globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8="
	google.com.             3600    IN      TXT     "v=spf1 include:_spf.google.com ~all"
	google.com.             3600    IN      TXT     "apple-domain-verification=30afIBcvSuDV2PLX"
	google.com.             3600    IN      TXT     "google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ"
	google.com.             3600    IN      TXT     "docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e"
	google.com.             3600    IN      TXT     "google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o"

	```
4. Query **MX** records - get list of all the mail servers for a specific domain, use the `mx` option:
	```shell
	$ dig +nocmd google.com mx +noall +answer
	google.com.             600     IN      MX      20 alt1.aspmx.l.google.com.
	google.com.             600     IN      MX      10 aspmx.l.google.com.
	google.com.             600     IN      MX      30 alt2.aspmx.l.google.com.
	google.com.             600     IN      MX      50 alt4.aspmx.l.google.com.
	google.com.             600     IN      MX      40 alt3.aspmx.l.google.com.
	```
5. Query **NS** records = find the authoritative name servers for specific domain, use the `ns` option:
	```shell
	$ dig +nocmd google.com ns +noall +answer
	google.com.             342334  IN      NS      ns1.google.com.
	google.com.             342334  IN      NS      ns2.google.com.
	google.com.             342334  IN      NS      ns4.google.com.
	google.com.             342334  IN      NS      ns3.google.com.
	```

## Reverse DNS Lookup
Query the hostname associated with a specific IP address by using the `-x` option.

Perform a revers lookup on 208.118.235.148:
```shell
$ dig -x 208.118.235.148 +noall +answer
; <<>> DiG 9.13.3 <<>> -x 208.118.235.148 +noall +answer
;; global options: +cmd
148.235.118.208.in-addr.arpa. 245 IN	PTR	wildebeest.gnu.org.
```
From the above output, the IP address 208.118.235.148 is associated with the hostname wildebeest.gnu.org.



```shell
$ dig -x 208.118.235.148 +noall +answer
148.235.118.208.in-addr.arpa. 86400 IN  PTR     ip-208-118-235-148.twdx.net.

```


## Settings
The `.digrc` file is present in the user's home directory, the options specified in it are applied before the command line arguments.

For example, if you want to only display the answer section, update the `~/.digrc` file:


`~/.digrc` file:
```
+nocmd +noall +answer
```



## Refences
1. https://linuxize.com/post/how-to-use-dig-command-to-query-dns-in-linux/
