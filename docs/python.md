- [Environment](#environment)
- [OS Environment Variables](#os-environment-variables)
- [Pip Module](#pip-module)
- [Regular Expressions](#regular-expressions)
  - [match vs search](#match-vs-search)
  - [findall vs finditer](#findall-vs-finditer)
  - [Lookaheads And Lookbehinds](#lookaheads-and-lookbehinds)
    - [Look Ahead Positive (?=)](#look-ahead-positive-)
    - [Look ahead negative (?!)](#look-ahead-negative-)
    - [Look behind positive (?\<=)](#look-behind-positive-)
    - [Look behind negative (?\<!)](#look-behind-negative-)
  - [Python RegEx Sources](#python-regex-sources)
- [Threads](#threads)
  - [Example Threading](#example-threading)
  - [Daemon Threads](#daemon-threads)
  - [Example Daemon Threading](#example-daemon-threading)
  - [Example Multi-Threading](#example-multi-threading)
- [Unittesting](#unittesting)
  - [Writing Tests](#writing-tests)
  - [Example UnitTest](#example-unittest)
  - [Assert Methods](#assert-methods)
  - [Running Unittests](#running-unittests)
    - [Run Tests as executable in main](#run-tests-as-executable-in-main)
    - [Run Tests Through CLI](#run-tests-through-cli)
  - [Code Coverage](#code-coverage)
    - [Example Code Coverage](#example-code-coverage)
- [Output](#output)
  - [Print Numbers By Base](#print-numbers-by-base)

```shell
# check version
python --version
```

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

# Environment

```shell
# create virtual environment
python3 -m venv {environment_name}

# activate environment
source virtual_environment_directory/bin/activate

# exit environment
deactivate
```

# OS Environment Variables

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

# Pip Module

```shell
# search if python package is installed
python3 -m pip search {package_name}

# list installed packages
python3 -m pip freeze

# install python packages
python3 -m pip install {package_name}

# install from packages from file
python3 -m pip install -r requirements.txt
```

# Regular Expressions

```python
# Not needing to compile
num = "<some_regex>"
m = re.match(num, <some_text>)

# Versus compiling:
num = re.compile("<some_regex>")
m = num.match(<some_text>)
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

## Python RegEx Sources

- [findall() vs finditer()](https://stackoverflow.com/a/4697884/14745606)
- [match() vs search()](https://testdriven.io/tips/421e050b-176b-4a72-a8b5-6ad5f185b86a/#:~:text=match%20in%20Python%3F-,re.,matches%20anywhere%20in%20the%20string.)
- [Lookaheads And Lookbehinds](https://stackoverflow.com/a/2973495/14745606)

# Threads

Enable concurrent execution within a single process. A sequence of instructions within a program that can be executed independently of other code (a subset of a process).

## Example Threading

```python
# Implement threading within a program.
import logging
import threading
import time

def some_function(name: str):
    logging.info(f'{name} THREAD: starting')
    time.sleep(3)
    logging.info(f'{name} THREAD: finishing')

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

logging.info('MAIN: before creating thread')
t = threading.Thread(target=some_function, args=(1,))
logging.info('MAIN: before starting thread')
t.start()
logging.info('MAIN: thread running')

# use join() to wait for thread to complete before proceeding
# t.join()
logging.info('MAIN: all done')
```

Output

> Notice `Thread 1` is running on it's own thread & even finishes after the main program exits. `Thread 1` is not a daemon thread, meaning the main program does not have to wait for it to finish in order for itself to complete.

```log
12:11:02: MAIN: before creating thread
12:11:02: MAIN: before starting thread
12:11:02: 1 THREAD: starting
12:11:02: MAIN: thread running
12:11:02: MAIN: all done
12:11:05: 1 THREAD: finishing
```

Output when using `join()` method to ensure thread completes before main exists.

> Joining threads will ensure the program to wait for the joined thread(s) to finish before proceeding.

```log
12:11:20: MAIN: before creating thread
12:11:20: MAIN: before starting thread
12:11:20: 1 THREAD: starting
12:11:20: MAIN: thread running
12:11:23: 1 THREAD: finishing
12:11:23: MAIN: all done
```

## Daemon Threads

Background threads that automatically terminate when the main program exists.

Daemon threads will shut down immediately when the main program completes. If threads are running that are not daemon, the main program will wait for those threads to complete before exiting. However, uncompleted *daemon* threads will be terminated once the main program exits.

When a python program exits, part of the shutdown process is cleaning up threading routines. `threading._shutdown()` iterates through all running threads and calls `.join()` on each that do not have a daemon flag set as True.

## Example Daemon Threading

```python
# Implement daemon threading within a program, which will shut down immediately when the main program exists.
import logging
import threading
import time

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

def some_function(name: str):
    logging.info(f'{name} THREAD: starting')
    time.sleep(3)
    logging.info(f'{name} THREAD: finishing')

logging.info('MAIN: before creating thread')
t = threading.Thread(target=some_function, args=('DAEMON',), daemon=True)
logging.info('MAIN: before starting thread')
t.start()
logging.info('MAIN: thread running')
logging.info('MAIN: all done')
```

output

> `DAEMON` thread is terminated once the main program completes.

```log
12:11:38: MAIN: before creating thread
12:11:38: MAIN: before starting thread
12:11:38: DAEMON THREAD: starting
12:11:38: MAIN: thread running
12:11:38: MAIN: all done
```

## Example Multi-Threading

```python
# Implement multi-threading within a program.
import logging
import threading
import time

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

def some_function(name: str):
    logging.info(f'{name} THREAD: starting')
    time.sleep(3)
    logging.info(f'{name} THREAD: finishing')

if __name__ == '__main__':
    start = time.time()
    use_join = True
    thread_list = []

    logging.info('MAIN: before creating multi-threads')
    for i in range(5):
        t = threading.Thread(target=some_function, name=f'{i}', args=(i,))
        thread_list.append(t)
        t.start()

    if (use_join):
        logging.info('MAIN: wait for multi-threads to finish')
        for index, t in enumerate(thread_list):
            logging.info(f"MAIN: joining thread {index}.")
            t.join()
    end = time.time()
    logging.info(f'MAIN: all done, finished in {end-start} seconds')
```

Output

> Since we are joining these threads, the main program will not exit without completing each one (regardless if `daemon=True`).

```log
12:24:47: MAIN: before creating multi-threads
12:24:47: 0 THREAD: starting
12:24:47: 1 THREAD: starting
12:24:47: 2 THREAD: starting
12:24:47: 3 THREAD: starting
12:24:47: 4 THREAD: starting
12:24:47: MAIN: wait for multi-threads to finish
12:24:47: MAIN: joining thread 0.
12:24:50: 0 THREAD: finishing
12:24:50: 1 THREAD: finishing
12:24:50: MAIN: joining thread 1.
12:24:50: MAIN: joining thread 2.
12:24:50: 2 THREAD: finishing
12:24:50: MAIN: joining thread 3.
12:24:50: 3 THREAD: finishing
12:24:50: 4 THREAD: finishing
12:24:50: MAIN: joining thread 4.
12:24:50: MAIN: all done, finished in 3.0058000087738037 seconds
```

# Unittesting

## Writing Tests

Create a test case by subclassing `unittest.TestCase`

Each individual test is defined with methods whose names begin with "test".

Initialize both the `setUp()` and `tearDown()` methods to define instructions that will be executed before and after each test method.

## Example UnitTest

```python
import unittest

class TestCaseNameHere(unittest.TestCase):
    def setUp(self):
        # method called for every single test defined
        self.isWorking = true

    def test_toggle(self)
        # test toggling the boolean value
        self.assertNotEqual(isWorking, false);

    def tearDown(self):
        # tidies up code after each test is run
        # useful for removing any data created during tests
        pass
```

## Assert Methods

| Syntax                   | Description         |
| :---                     | ---:                |
| assertEqual(a,b)         | a == b              |
| assertNotEqual(a,b)      | a != b              |
| assertTrue(x)            | bool(x) is True     |
| assertFalse(x)           | bool(x) is False    |
| assertIs(a,b)            | a is b              |
| assertIsNot(a,b)         | a is not b          |
| assertIsNone(x)          | x is None           |
| assertIsNotNone(x)       | x is not None       |
| assertIn(a,b)            | a in b              |
| assertNotIn(a,b)         | a not in b          |
| assertIsInstance(a,b)    | isinstance(a,b)     |
| assertNotIsInstance(a,b) | not isinstance(a,b) |

Extra assert methods:

| Syntax                    | Description         |
| :---                      | ---:                |
| assertAlmostEqual(a,b)    | round(a-b,7) == 0   |
| assertNotAlmostEqual(a,b) | round(a-b, 7) != 0  |
| assertGreater(a,b)        | a > b               |
| assertGreaterEqual(a,b)   | a >= b              |
| assertLess(a,b)           | a < b               |
| assertLessEqual(a,b)      | a <= b              |
| assertRegex(s,r)          | r.search(s)         |
| assertNotRegex(s,r)       | not r.search(s)     |
| assertCountEquals(a,b)    | a and b have the same number of elements, regardless of their order |

## Running Unittests

### Run Tests as executable in main

Utilize the `unittest.main()` method in the test file's main.

```python
if __name__ == '__main__':
    unittest.main()

    # Or run tests with more higher verbosity for more detailed information:
    # unittest.main(verbosity=2)
```

### Run Tests Through CLI

Run a tests from the command line interface:

```shell
# run multiple test modules
python -m unittest test_module_one test_module_two

# run specific TestClass of a test module
python -m unittest test_module_one.TestClassName

# run specific test method
python -m unittest test_module_one.TestClassName.test_method

# run test from given path
python -m unittest tests/test_file.py

# run test with higher verbosity
python -m unittest -v test_module_one

# run without arguments to start Test Discovery
python -m unittest
# or
python -m unittest discover
```

> Test Discovery will find all test modules by recursing into subdirectories.

## Code Coverage

Code coverage is the degree to which the source code of a program is executed (covered) by automated tests.

Measured by a percentage, where higher percentage of coverage has more of its source code executed during testing.

Code coverage determines which statements in a body of code have been executed through a test run, and which statements have not.

Install python library containing code analysis tools and tracing hooks to determine which lines are executable, and which have been executed: `python3 -m pip install coverage`

Usage: `coverage run <options> <program>`

- Coverage Options
  - `source`: specify source to measure, only source inside given directories or packages will be measured
  - `include`: specify files matching the given patterns to be measured
  - `omit`: specify files matching the given patterns not to be measured

### Example Code Coverage

```shell
# run coverage on test_encryption program
coverage run --source="." test_encryption.py

# get coverage report
coverage report

# generate coverage text annotation
coverage annotate

# generate coverage text annotation files in a certain directory
coverage annotate -d coverage_files/

# run code coverage while running unittesting in discovery mode:
python -m coverage run -m unittest discover <test_directory>

python3 -m coverage run --source="." -m unittest discover
```

Output:

```shell
Name                 Stmts   Miss  Cover
----------------------------------------
code_file.py           21      2    90%
test_code_file.py      25      0   100%
----------------------------------------
TOTAL                   46      2    96%
```

Generated Text Annotation Prefix Values:

```txt
| Character | Meaning                |
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |
```

# Output

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
