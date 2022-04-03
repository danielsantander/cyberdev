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