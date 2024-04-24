- [Check Version](#check-version)
- [Create Python Virtual Environment](#create-python-virtual-environment)
- [Environment Variables](#environment-variables)
- [Tips](#tips)
  - [Append Paths](#append-paths)
  - [Make script executable](#make-script-executable)
  - [Pip Module](#pip-module)
  - [Print Numbers By Base](#print-numbers-by-base)
  - [Upgrade Python distribution](#upgrade-python-distribution)

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

# Check Version

Enter into terminal:

```shell
python --version
```

# Create Python Virtual Environment

```shell

# create environment
python3 -m venv {environment_name}

# activate environment
source virtual_environment_directory/bin/activate

# exit environment
deactivate
```

# Environment Variables

```python
import os

# set environment variable
os.environ.setdefault("LINEUP", "develop")

# retrieve OS environment variables
LINEUP = os.environ.get('develop', 'some_default_value')
```

# Tips

## Append Paths

```python
import os, sys

src_paths = ['/home/user/code/src', '/home/app']
for path in src_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)
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
