- [Metasploit](#metasploit)
  - [wmap](#wmap)

```shell
apt update && apt full-upgrade -y
```

# Metasploit

```shell
# open Metasploit
msfconsole

# open Metasploit without header
msfconsole -q

# ensure postgresql is started
sudo service --status-all | grep "postgresql"
sudo service postgresql start

```

## wmap

wmap utility will scan a list of URLs to test whether the web server exhibits security flaws.

> Ensure you run the utility on a website you own.

```shell
# load wmap framework plugin
msf6> load wmap

# run against a target
msf6> wmap_targets -t https://0.0.0.0
```
