The `diff` command runs a diff function on Git data sources such as: commits, branches, files, etc.

Usage: `git diff`


# diff options

## name status
Show names and status of changed files.

Usage: `git diff --name-status`

*Example*: Use the diff command to show all changed files on a given branch.
```shell
git diff --name-status <branch_name>
```

*Example*: use the same command but pipe with grep go search for changed files named "testFiles"
```shell
git diff --name-status <branch_name> | grep "testFile[s]"
```
