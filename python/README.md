
*Documentation*
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
│   └── threading/
└── scripts
    ├── README.md
    ├── encryptPDF.py
    ├── tests/
    └── utils
        ├── __init__.py
        ├── __pycache__
        ├── ciphers
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
$ chmod +x <python_script>.py
```
