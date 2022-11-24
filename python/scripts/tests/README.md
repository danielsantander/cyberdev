# Python Unit Testing


[source](https://docs.python.org/3/library/unittest.html)

# Run from CLI
Use unittest from the command line to run tests from modules, classes and individual test methods.

```shell
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method

python -m unittest tests/test_something.py
```

Test specific class such as TestFileHelper from test_utils.py file.
```shell
python3 -m unittest test_utils.TestFileHelper
```

# Run Tests With Coverage
Example of running unit tests with code coverage:
```shell
$ python -m coverage run -m unittest test_module
.
----------------------------------------------------------------------
Ran 5 tests in 0.012s

OK
```

# Gather Code Coverage Data
After running unit testing with code coverage, gather the results.
```shell
# get coverage report
$ coverage report

# generate coverage text annotation files in a given directory
$ coverage annotate -d coverage_files/
```

Output should look similar to the following
```shell
$ coverage report
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
python/scripts/tests/test_ciphers.py                29      0   100%
python/scripts/tests/test_contants.py               25      0   100%
python/scripts/tests/test_custom_exceptions.py      47      0   100%
python/scripts/tests/test_custom_logging.py         35      0   100%
python/scripts/tests/test_date_helper.py            29      0   100%
python/scripts/tests/test_file_helper.py           143      0   100%
python/scripts/tests/test_image_helper.py           58      0   100%
python/scripts/tests/test_navigation.py             66      0   100%
python/scripts/tests/test_validation.py             41      0   100%
python/scripts/utils/__init__.py                     0      0   100%
python/scripts/utils/ciphers/__init__.py             1      0   100%
python/scripts/utils/ciphers/caesar.py              31      0   100%
python/scripts/utils/constants.py                    1      0   100%
python/scripts/utils/custom_exceptions.py           22      0   100%
python/scripts/utils/custom_logging.py              37      0   100%
python/scripts/utils/date_helper.py                 11      0   100%
python/scripts/utils/file_helper.py                 87      0   100%
python/scripts/utils/image_helper.py                41      0   100%
python/scripts/utils/navigation.py                  22      0   100%
python/scripts/utils/validation.py                  13      0   100%
--------------------------------------------------------------------
TOTAL                                              739      0   100%
```

**Example 2**
```shell
$ python -m coverage run --source="." -m unittest discover python/scripts/tests/
$ coverage report
$ coverage annotate -d coverage_files/
```

## Annotation Prefix Values
Generated Text Annotation Prefix Values:
| Character | Meaning                |
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |