# Python Unit Testing


[source](https://docs.python.org/3/library/unittest.html)

## Run from CLI
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

## Run Tests With Coverage
Example of running unit tests with code coverage:
```shell
$ python -m coverage run -m unittest test_module
.
----------------------------------------------------------------------
Ran 5 tests in 0.012s

OK
```

## Gather Code Coverage Data
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
Name                                                   Stmts   Miss  Cover
--------------------------------------------------------------------------

--------------------------------------------------------------------------
TOTAL                                                    
```

Generated Text Annotation Prefix Values:
| Character | Meaning                |
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |