
- [Writing Tests](#writing-tests)
  - [Assert Methods](#assert-methods)
- [Running Tests](#running-tests)
  - [As an executable inside main](#as-an-executable-inside-main)
  - [Through CLI](#through-cli)
- [Code Coverage](#code-coverage)
  - [coverage.py](#coveragepy)


# Writing Tests
Create a test case by subclassing `unittest.TestCase`

Each individual test is defined with methods whose names begin with "test".

Initialize both the `setUp()` and `tearDown()` methods to define instructions that will be executed before and after each test method.

**Example**: Create a test case.

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

# Running Tests

## As an executable inside main
Utilize the `unittest.main()` method in the test file's main method.
```python
import unittest

# ...
# unittest.TestCase class and test cases here
# ...

if __name__ == '__main__':
    unittest.main()

    # Or run tests with more higher verbosity for more detailed information:
    # unittest.main(verbosity=2)
```

## Through CLI

Run a tests from the command line interface:
```shell

# run multiple test modules
$ python -m unittest test_module_one test_module_two

# run specific TestClass of a test module
$ python -m unittest test_module_one.TestClassName

# run specific test method
$ python -m unittest test_module_one.TestClassName.test_method

# run test from given path
$ python -m unittest tests/test_file.py

# run test with higher verbosity
$ python -m unittest -v test_module_one

# run without arguments to start Test Discovery
$ python -m unittest
# or
$ python -m unittest discover
```

> Test Discovery will find all test modules by recursing into subdirectories.

# Code Coverage
Code coverage is the degree to which the source code of a program is executed (covered) by automated tests.

Measured by a percentage, where higher percentage of coverage has more of its source doe executed during testing. 

Code coverage determines which statements in a body of code have been executed through a test run, anc which statements have not.

## coverage.py
Python library containing code analysis tools and tracing hooks to determine which lines are executable, and which have been executed.

> python -m pip install coverage

Usage: `coverage run <program>`

**Coverage Options**
- `source`: specify source to measure, only source inside given directories or packages will be measured
- `include`: specify files matching the given patterns to be measured
- `omit`: specify files matching the given patterns not to be measured

**Example**:: Use coverage to run program and gather data
```bash
# run coverage on test_encryption program
$ coverage run --source="." test_encryption.py

# get coverage report
$ coverage report

# generate coverage text annotation
$ coverage annotate

# generate coverage text annotation files in a certain directory
$ coverage annotate -d coverage_files/

```

Output should look similar to the following
```
Name                 Stmts   Miss  Cover
----------------------------------------
encryption.py           21      2    90%
test_encryption.py      25      0   100%
----------------------------------------
TOTAL                   46      2    96%
```

Generated Text Annotation Prefix Values:
| Character | Meaning                |
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |

