The `status` command displays paths in the working tree that are not currently tracked by git. It also displays paths that have differences between the following:
- index file and the current `HEAD` commit
- working tree and the index file

Usage: `git status`

# status options

## uall
Show individual files in untracked directories

Usage: `git status -uall`


## ignored
Show ignored files.

Usage: `git status --ignored`

*Example*: Show a list of all the files missing in the repository.
```shell
$ git status -uall --ignored
```