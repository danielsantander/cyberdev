- [Tips](#tips)
  - [Check Python Version](#check-python-version)
  - [Upgrade Python distribution](#upgrade-python-distribution)
  - [Make script executable](#make-script-executable)
- [Create Python Environment](#create-python-environment)
- [Pip Module](#pip-module)
- [Print Numbers By Base](#print-numbers-by-base)

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

# Tips
## Check Python Version
Enter into terminal:
```shell
python -V
Python 3.9.2
```

## Upgrade Python distribution
```shell
sudo apt-get upgrade python3
```

## Make script executable
Enter the following into the terminal:
```shell
$ sudo chmod +x <python_file>

# or
$ sudo chmod 755 <python_file>
```

# Create Python Environment
```shell

# create environment
python3 -m venv {environment_name}

# activate environment
source virtual_environment_directory/bin/activate
```
> Exit the environment with the `deactivate` command

# Pip Module
Search if python package is installed
```shell
python -m pip search {package_name}
```

Install python packages
```shell
python -m pip install {package_name}
```

# Print Numbers By Base

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