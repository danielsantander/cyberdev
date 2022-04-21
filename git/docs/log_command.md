
Check logs for a given branch:  `git log <branch_name>`

# log options

## oneline
Simplified list of commits in one line each.

Usage: `git log --oneline`


## stat
Displays more detail (including which files changes)

Usage: `git log --stat`

## follow
List log commits for specific file.

Usage: `git log --follow <filename>`

> `filename` accepts a path, which can be either a file or a directory.


# Log Tips
## View commit differences between branches

**Example**: Utilizing the `--oneline` option, display commits that develop branch has but main branch does not.
```shell
$ git log main..develop --oneline
```

## List all commits for specific file

**Example**: list all commits for readme file
```shell
$ git log --oneline --follow git/docs/README.md
```