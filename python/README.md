
- [Regular Expressions](#regular-expressions)
  - [match vs search](#match-vs-search)
  - [findall vs finditer](#findall-vs-finditer)
  - [Lookaheads And Lookbehinds](#lookaheads-and-lookbehinds)
    - [Look Ahead Positive (?=)](#look-ahead-positive-)
    - [Look ahead negative (?!)](#look-ahead-negative-)
    - [Look behind positive (?\<=)](#look-behind-positive-)
    - [Look behind negative (?\<!)](#look-behind-negative-)
- [Libraries](#libraries)
  - [scapy](#scapy)
- [Tips](#tips)
  - [Append Sys Paths](#append-sys-paths)
  - [Environment Variables](#environment-variables)
  - [Make script executable](#make-script-executable)
  - [Pip Module](#pip-module)
  - [Print Numbers By Base](#print-numbers-by-base)
  - [Upgrade Python distribution](#upgrade-python-distribution)
- [API](#api)
  - [NASA](#nasa)
  - [RedditAPI](#redditapi)
- [Tests](#tests)

---

More Docs:

- [Ciphers](docs/ciphers.md)
  - [Caesar Cipher](docs/ciphers.md#caesar-cipher)
    - [Encrypt Caesar Cypher](docs/ciphers.md#encrypt-caesar-cipher)
    - [Decrypt Caesar Cypher](docs/ciphers.md#decrypt-caesar-cipher)
- [Unit Testing](docs/unittesting.md)
  - [Writing Tests](docs/unittesting.md#writing-tests)
  - [Running Tests](docs/unittesting.md#running-tests)
  - [Code Coverage](docs/unittesting.md#code-coverage)
- [Threading](docs/threading.md)
  - [Daemon Threads](docs/threading.md#daemon-threads)
  - [Join Threads](docs/threading.md#joining-threads)

---

```shell
# check version
python --version

# create virtual environment
python3 -m venv {environment_name}

# activate environment
source virtual_environment_directory/bin/activate

# exit environment
deactivate
```

# Regular Expressions

Not needing to compile vs compiling.

```python
num = "..."
m = re.match(num, input)

# Versus compiling:
num = re.compile("...")
m = num.match(input)
```

> compiling allows you to separate definition of the regex from its use

Ignore case sensitivity by passing `re.IGNORECASE` to the flags param of `search`, `match`, or `sub`.

```python
m = num.match(input, re.IGNORECASE)
```

## match vs search

- `re.match()` searches for matches from the beginning of a string
- `re.search()` searches for matches anywhere in the string.

```python
import re

txt = 'Hello world!'

print(re.search(r'world', txt).group())
# => world

print(re.match(r'world', txt))
# => None

print(re.search(r'Hello', txt).group())
# => Hello

print(re.match(r'Hello', txt).group())
# => Hello
```

## findall vs finditer

- `re.findall(pattern, string)` returns a list of matching strings.
- `re.finditer(pattern, string)` returns an iterator over MatchObject objects.

```python
import re
re.findall( r'all (.*?) are', 'all cats are smarter than dogs, all dogs are dumber than cats')
# => ['cats', 'dogs']

[x.group() for x in re.finditer( r'all (.*?) are', 'all cats are smarter than dogs, all dogs are dumber than cats')]
# => ['all cats are', 'all dogs are']
```

## Lookaheads And Lookbehinds

Given the string `foobarbarfoo`:

```text
bar(?=bar)     finds the 1st bar ("bar" which has "bar" after it)
bar(?!bar)     finds the 2nd bar ("bar" which does not have "bar" after it)
(?<=foo)bar    finds the 1st bar ("bar" which has "foo" before it)
(?<!foo)bar    finds the 2nd bar ("bar" which does not have "foo" before it)
```

You can also combine them:

```text
(?<=foo)bar(?=bar)    finds the 1st bar ("bar" with "foo" before it and "bar" after it)
```

### Look Ahead Positive (?=)

Find expression A where expression B follows: `A(?=B)`

### Look ahead negative (?!)

Find expression A where expression B does not follow: `A(?!B)`

### Look behind positive (?<=)

Find expression A where expression B precedes: `(?<=B)A`

### Look behind negative (?<!)

Find expression A where expression B does not precede: `(?<!B)A`

---

Python RegEx Sources:

- [findall() vs finditer()](https://stackoverflow.com/a/4697884/14745606)
- [match() vs search()](https://testdriven.io/tips/421e050b-176b-4a72-a8b5-6ad5f185b86a/#:~:text=match%20in%20Python%3F-,re.,matches%20anywhere%20in%20the%20string.)
- [Lookaheads And Lookbehinds](https://stackoverflow.com/a/2973495/14745606)

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
> `src 10.0.0.100` specifies  a filter that captures only packets originating on machine 10.0.0.100
>
> `dst 10.0.0.100`, which captures only packets with a destination of 10.0.0.100
>
> `tcp port 110 or tcp port 25` specifies a filter that will pass only TCP packets coming from or going to port 110 or 25.
>
> `tcp port 21` to watch for FTP connections

# Tips

## Append Sys Paths

```python
import os, sys

src_paths = ['/home/user/code/src', '/home/app']
for path in src_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

        # insert at beginning
        # sys.path.insert(0, path)
```

## Environment Variables

```python
import os

# set environment variable
os.environ.setdefault("LINEUP", "develop")

# retrieve OS environment variables
lineup_env_var = os.environ.get('LINEUP', 'local')

# retrieve a "list" environment variable
import json
env_list = json.loads(os.environ.get('env_list', '["default_value_one", "default_value_two"]'))
```

## Make script executable

Enter the following into the terminal:

```shell
sudo chmod +x <python_file>

# or
sudo chmod 755 <python_file>
```

## Pip Module

```shell
# search if python package is installed
python -m pip search {package_name}

# install python packages
python -m pip install {package_name}

# install from packages from file
python -m pip install -r requirements.txt
```

## Print Numbers By Base

Print binary: `{number}:{width}{base}`

```python
>>> num = 100
>>> width = 4
>>> base = 'b'
>>> bases = 'dXob'
>>> print ('{num:{width}{base}}'.format(num=num,width=width,base=base))
 101

>>> num = 42
>>> bases = 'dXob'
>>> for base in bases:
# ...     print ('{num:0{width}{base}}'.format(num=num,width=width,base=base))  # add '0' for leading zeros
...     print ('{num:{width}{base}}'.format(num=num,width=width,base=base))
...
  42
  2A
  52
101010
```

## Upgrade Python distribution

```shell
# for linux:
sudo apt-get upgrade python3
```

# API

## NASA

Before using the `nasa.py` script, enter your `NASA_API_KEY` within the `.env` file and run `. .env`.

Saved files will be located in the same directory at:  `./api_data/nasa/`

```shell
usage: ./nasa.py [data]

# example: retrieve data from EPIC satellite
python3 nasa.py epic
Use enhanced images (Y/N)?: Y

# example to retrieve data from Mars Curiosity rover.
# (earth date in format: YYYY-MM-DD)
python3 nasa.py curiosity
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
import RedditAPI
from pathlib import Path

save_directory_path = Path("/some/save/directory/path/")

reddit = RedditAPI(
  client_id="enter_client_id_here",
  client_secret="enter_cilent_secret_here",
  username="enter_username_here",
  password="enter_password_here"
  save_dir=save_directory_path,
  use_verbose=True,)

# retrieve user's saved posts data, returns dictionary of data
saved_data = reddit.get_saved_data()

# unsave a given post, returns the response
resp = reddit.unsave_post(post_dict)
```

When using interactively through the shell, ensure the environment variables are set within `.env` (copied from `.dev.env`) and run `. .env` for the script to pick up the credentials. Then proceed.

Some Examples:

```shell
# get_saved: get user's saved data and save to a given directory
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

# Tests

```shell
# Run all tests found in directory
python3 -m unittest discover <test_directory>

# Run a single test
python3 test_api.py

# run code coverage while running unittesting in discovery mode:
python3 -m coverage run -m unittest discover <test_directory>

# Run with code coverage
coverage run --source="." test_api.py

# get coverage report
coverage report

# save coverage files
mkdir coverage_files/
coverage annotate -d coverage_files/
```

Generated Text Annotation Prefix Values:

| Character | Meaning                |
|-----------|------------------------|
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |
