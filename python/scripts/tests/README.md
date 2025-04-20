# Python Unit Testing

[source](https://docs.python.org/3/library/unittest.html)

Use unittest from the command line to run tests from modules, classes and individual test methods.

```shell
# Examples:
python3 -m unittest test_module1 test_module2
python3 -m unittest test_module.TestClass
python3 -m unittest test_module.TestClass.test_method
python3 -m unittest tests/test_something.py

# Test specific class such as TestFileHelper from test_utils.py file.
python3 -m unittest test_utils.TestFileHelper

# Run Tests With Coverage
python3 -m coverage run -m unittest test_module

# Gather Code Coverage Data
coverage report

# Generate annotated files in directory
coverage annotate -d coverage_files/

# Example 2
python3 -m coverage run --source="." -m unittest discover .
```

## Annotation Prefix Values

Generated Text Annotation Prefix Values:

| Character | Meaning                |
|-----------|------------------------|
| :---      | ---:                   |
| >         | executed               |
| !         | missing (not executed) |
| -         | excluded               |

