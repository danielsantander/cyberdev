- [git stash](#git-stash)
  - [Stash Specified Files](#stash-specified-files)
- [Undo Changes](#undo-changes)
  - [git checkout](#git-checkout)
  - [git reset](#git-reset)
  - [git clean](#git-clean)
  - [tips](#tips)
- [Sources](#sources)

---
*Table of Contents*
- [Configuration](configuration.md)
- [Branching Strategy](branching_strategy.md)
- [Diff Command](diff_command.md)
- [Log Command](log_command.md)
- [Pull Command](pull_command.md)
- [Stash Command](stash_command.md)
- [Status Command](status_command.md)
- [Tips](tips.md)
  - [List Branches By Order](tips.md#list-branches-by-order)
  - [Update](tips.md#update)
  - [Move files from one branch into current](tips.md#move-files-from-one-branch-into-current)
  - [Pull files from another commit](tips.md#pull-files-from-another-commit)
  - [Ignore already tracked files](tips.md#ignore-already-tracked-files)

# git stash

**Usage:**

```shell
# list
git stash list

# show changes recorded in stash as diff
git stash show [-u|--include-untracked|--only-untracked] [<diff-options>] [<stash>]

# deprecated in favour of git stash push. It differs from "stash push" in that it cannot take pathspec.
git stash save [-p|--patch] [-S|--staged] [-k|--[no-]keep-index] [-u|--include-untracked] [-a|--all] [-q|--quiet] [<message>]

# save local modifications to a new stash entry and roll them back to HEAD, can omit "push"
git stash push [-p|--patch] [-S|--staged] [-k|--[no-]keep-index] [-u|--include-untracked] [-a|--all] [-q|--quiet] [(-m|--message) <message>] [--pathspec-from-file=<file> [--pathspec-file-nul]] [--] [<pathspec>…​]
```

## Stash Specified Files

```shell
git stash push path/to/file
```

# Undo Changes

## git checkout

Reset specific file to last committed state (to discard uncommitted changes in a specific file):

```shell
git checkout ExampleFile.txt
git checkout -- ExampleFile.txt
```

## git reset

Reset entire repository to the last committed state:

```shell
git reset --hard
```

## git clean

Remove untracked files, usage: `git clean [-d] [-f] [-i] [-n] [-q] [-e <pattern>] [-x | -X] [--] [<pathspec>…]`

```shell
git clean -df
```

Where options are:
| Flag          |  Description                                                  |
| --------------|---------------------------------------------------------------|
| -d            | with no <pathspec>, specify `-d`to recurse into directories   |
| -f, --force   | enable to delete fiels or directories, otherwise will refuse  |
| -n, --dry-run | don't remove anything,show what would be done                 |

## tips

Quickly undo staged and/or unstaged chagnes. [src](https://stackoverflow.com/a/21396698/14745606)
```shell
git reset HEAD  # unstage all changes
git checkout .  # discard all changes
```

Alternative way to restore *unstaged* files. If a file has both staged and unstaged changes, only the unstaged changes shown in git diff are reverted. Changes shown in git diff --staged stay intact. [src](https://stackoverflow.com/a/52713/14745606)
```shell
# for all unstaged files
git restore .

# for a specific file
git restore path/to/file/to/revert
```

# Sources

- [git reset](https://git-scm.com/docs/git-reset)
- [git stash](https://git-scm.com/docs/git-stash)