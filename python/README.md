
**Table of Contents**
- [Ciphers](docs/ciphers.md)
  - [Caesar Cipher](docs/ciphers.md#caesar-cipher)
    - [Encrypt Caesar Cypher](docs/ciphers.md#encrypt-caesar-cipher)
    - [Decrypt Caesar Cypher](docs/ciphers.md#decrypt-caesar-cipher)
- [Docker](docs/docker.md)
- [Unit Testing](docs/unittesting.md)
  - [Writing Tests](docs/unittesting.md#writing-tests)
  - [Running Tests](docs/unittesting.md#running-tests)
  - [Code Coverage](docs/unittesting.md#code-coverage)
- [Threading](docs/threding.md)
  - [Daemon Threads](docs/threding.md#daemon-threads)
  - [Join Threads](docs/threding.md#joining-threads)

# Python
Python documentation and scripts.

Contents:
```
├── README.md
├── docs
│   ├── README.md
│   ├── ciphers.md
│   ├── docker.md
│   ├── threding.md
│   └── unittesting.md
├── examples
│   ├── docker
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── src
│   └── threading
│       ├── daemon_thread.py
│       ├── multithread.py
│       └── threads.py
└── scripts
    ├── README.md
    ├── encryptPDF.py
    ├── rename_screenshot_files.py
    ├── tests
    │   ├── README.md
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── sample_data
    │   ├── test_ciphers.py
    │   └── test_utils.py
    └── utils
        ├── __init__.py
        ├── __pycache__
        ├── ciphers/
        ├── custom_exceptions.py
        ├── custom_logging.py
        ├── date_helper.py
        ├── file_helper.py
        ├── image_helper.py
        ├── logs
        ├── navigation.py
        └── validation.py
```

Python scripts should contain the following shebang: `#!/usr/bin/python3`

## Check Python Version
Enter into terminal:
```shell
$ python -V
Python 3.9.2
```

## Make script executable
Enter the following into the terminal:
```shell
$ sudo chmod +x <python_file>

# or
$ sudo chmod 755 <python_file>
```
