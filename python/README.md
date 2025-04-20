
- [Libraries](#libraries)
  - [scapy](#scapy)
- [Scripts](#scripts)
  - [Ciphers](#ciphers)
    - [Caesar Cipher](#caesar-cipher)
      - [Encrypt Caesar Cipher](#encrypt-caesar-cipher)
      - [Decrypt Caesar Cipher](#decrypt-caesar-cipher)
- [API](#api)
  - [NASA](#nasa)
  - [RedditAPI](#redditapi)
---

# Libraries

## scapy

Sniffer function:

```python
from scapy.all import sniff

def print_packet(packet):
  print (packet)
  return packet

sniff(filter="", iface="any", prn=function, count=N)
>>> sniff(filter="tcp port 80", prn=print_packet)
>>> sniff(filter="tcp port 443", prn=print_packet)
```

Where:

- `filter` is used to specify a Berkeley Packet Filter (BPF) to the packets sniffed, leaving blanks will sniff all packets.
  - Example, to sniff all HTTP packets, use BPF filter of `tcp port 80`
- `iface` is used to specify which network interface to sniff on. Leave blank to sniff on all interfaces.
- `prn` specifies a callback function to be called for every packet object with a single parameter.
- `count` specifies how many packets to sniff, if blank Scapy will sniff indefinitely.

Berkeley Packet Filter (BPF) Syntax:

| Expression | Description                   | Sample keywords      |
|------------|-------------------------------|----------------------|
| Descriptor | What your looking for         | host, net, port      |
| Direction  | Direction of travel           | src, dst, src or dst |
| Protocol   | Protocol used to send traffic | ip, ip6, tcp, udp    |

> examples:
> `src 10.0.0.100` specifies a filter that captures only packets originating on machine 10.0.0.100
>
> `dst 10.0.0.100`, which captures only packets with a destination of 10.0.0.100
>
> `tcp port 110 or tcp port 25` specifies a filter that will pass only TCP packets coming from or going to port 110 or 25.
>
> `tcp port 21` to watch for FTP connections

# Scripts

## Ciphers

### Caesar Cipher

A simple cipher that encrypts messages by replacing each letter with a new value determined by shifting the alphabet over a given offset value.

For example, with an offset value of 3 every A would be replaced by the letter D, every B with the letter E, every C with the letter F, and so on...

#### Encrypt Caesar Cipher

Using the Caesar cipher to encrypt a message without defining an offset value will default to shifting the message 3 alphabet letters.

For example, encrypting `Hello World` with the Caesar cipher and a default offset value of 3 will output `khoor zruog`.

```python
from utils.ciphers import caesar
caesar.encrypt("Hello World")

>>> 'khoor zruog'
```

Defining an offset of 15 will encrypt the message by shifting the alphabet 15 letters. Encrypting `Hello World` with an offset of 15 will return `wtaad ldgas`

```python
from utils.ciphers import caesar
caesar.encrypt("Hello World", offset=15)

>>> 'wtaad ldgas'
```

#### Decrypt Caesar Cipher

Decrypting a Caesar cipher message requires the known offset value. For example, decrypting the message `amkzmb umaaiom` will need an offset value of 8.

```python
from utils.ciphers import caesar
caesar.decrypt('amkzmb umaaiom', offset=8)

>>> 'secret message'
```

# API

Ensure to set any credentials within a `.env` file (copy `.env.dev.` as template), and run `. .env` to set variables.

## NASA

Before using the `nasa.py` script, enter your `NASA_API_KEY` within the `.env` file and run `. .env`.

Saved files will be located in the same directory at the default path:  `./api_data/nasa/`

```shell
# NASA_API_KEY optional if already in ENVIRONMENT
usage: ./nasa.py -a [action] -k [NASA_API_KEY]

# example: retrieve data from EPIC satellite
python3 nasa.py -a epic
Use enhanced images (Y/N)?: Y

# example to retrieve data from Mars Curiosity rover.
# (earth date in format: YYYY-MM-DD)
python3 nasa.py -a curiosity
Query by 'martian_sol' or 'earth_date': sol
Enter Sol date [1000]: 1001
```

## RedditAPI

Purposes: Utilize the Reddit API to retrieve and save media.

Setup:

- Visit [here](https://www.reddit.com/prefs/apps/) to generate client creds.
- Enter creds into the environment file `.env` (copied from `.dev.env`). Run `. .env` so script can read new variables.

Importing as module.

```python
import json
import os
from reddit import RedditAPI
from pathlib import Path

params = {
    "client_id": os.environ.get('REDDIT_CLIENT_ID'),
    "client_secret": os.environ.get('REDDIT_CLIENT_SECRET'),
    "username": os.environ.get('REDDIT_USERNAME'),
    "password": os.environ.get('REDDIT_PASSWORD'),
    "save_dir": Path() / 'api_data',
    "use_verbose": True,
}
reddit = RedditAPI(**params)

# retrieve user's saved post data, returns dictionary of posts
saved_data = reddit.get_saved_data()

# unsave a given post, returns the response
resp = reddit.unsave_post(post_dict)
```

Some Examples:

```shell
# get_saved: get user's saved data, retrieve media from source urls, and save to a given directory
./reddit.py -a get_saved -u -d -o /some/path/to/save_data_directory/
# where:
# - a: action
# - u: update (call API for fresh save data)
# - d: debug/verbose mode
# - o: output directory

# consolidate: retrieve past saved data and compile into a new file named "YYYYMMDDHHMMSS--consolidated_saved_data.json"
./reddit.py -a consolidate -o api_data/

# sanitize: retrieve and move files found within a provided list of blacklisted subs
./reddit.py -a sanitize -d -o api_data/
```

> excluding the output directory will save all api data within directory `api_data/`
