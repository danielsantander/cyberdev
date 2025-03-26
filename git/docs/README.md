- [Tips](#tips)
  - [Ignore Already Tracked Files](#ignore-already-tracked-files)
  - [List Branches By Order](#list-branches-by-order)
  - [Pull In Files From A Commit](#pull-in-files-from-a-commit)
  - [Pull In Files From Branch Into Current](#pull-in-files-from-branch-into-current)
  - [Update Branches](#update-branches)
- [Undo Changes](#undo-changes)
  - [git checkout](#git-checkout)
  - [git clean](#git-clean)
  - [git reset](#git-reset)
- [Sources](#sources)


---

# Tips

## Ignore Already Tracked Files

[src](https://stackoverflow.com/a/10755704/14745606)

```shell
# ignore and stop tracking a file
git update-index --assume-unchanged [<file> ...]

# start tracking file again
git update-index --no-assume-unchanged [<file> ...]
```

## List Branches By Order

```shell
# List **local** branches in order from recent to oldest with the given format
git for-each-ref --sort=-committerdate refs/heads/ --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'

# List **remote** branches in order from recent to oldest with the given format
git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'
```

## Pull In Files From A Commit

[src](https://stackoverflow.com/a/51719585/14745606)

**Example**: Pull in files from a commit into the currently checked out branch.

```shell
# Step 1: Checkout on the required branch.
git checkout develop

#Step 2: Make sure you have copied the required commit hash.
git checkout <commit_hash> <path_to_file>

# TIP: or if you want to copy ALL changed files FROM THAT CHANGESET:
git checkout <commit_hash> .

#Step 3: You now have the changes of the required file on your desired branch. You just need to add and commit them.
git add <path_to_file>
git commit -m "Your commit message"
```

## Pull In Files From Branch Into Current

**Example**: Pull files from localBranch into the currently checked out branch (develop)

```shell
git checkout develop
git checkout localBranch .
```

## Update Branches

```shell
# update remote branches
git remote update origin --prune

# update local branches
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
```

# Undo Changes

Quickly undo changes (staged & unstaged). [src](https://stackoverflow.com/a/21396698/14745606)

```shell
git reset HEAD  # unstage all changes
git checkout .  # discard all changes

# OR do the following

git reset --hard  # undo all staged changes
git clean -fd     # remove untracked files
```

Discard unstaged changes (restore files). [src](https://stackoverflow.com/a/52713/14745606)

```shell

git restore .                       # for all unstaged files in current working dir
git restore path/to/file/to/revert  # specify a file

# before Git 2.23:
git checkout -- .                       # for all unstaged files in current working dir
git checkout -- path/to/file/to/revert  # specify a file
```

## git checkout

Undo changes with `git checkout`

```shell
# recet file to last commited state (disgard uncommitted changes)
git checkout ExampleFile.txt
git checkout -- ExampleFile.txt


# Revert files to number commit
git checkout {has_commit_number} -- file1/to/restore file2/to/restore

# Revert files to number of commits (N) before a given commit
git checkout {has_commit_number}~N -- file1/to/restore file2/to/restore

# example: revert files one commit before given commit
git checkout {has_commit_number}~1 -- file1/to/restore file2/to/restore
```

## git clean

Remove untracked files, usage: `git clean [-d] [-f] [-i] [-n] [-q] [-e <pattern>] [-x | -X] [--] [<pathspec>…]`

```shell
git clean -df
```

> use `-n` instead of `-f` to perform a dry run and list which files will be deleted.

Where options are:
| Flag          |  Description                                                  |
| --------------|---------------------------------------------------------------|
| -d            | with no <pathspec>, specify `-d`to recurse into directories   |
| -f, --force   | enable to delete files or directories, otherwise will refuse  |
| -n, --dry-run | don't remove anything,show what would be done                 |

## git reset

Reset entire repository to the last committed state:

```shell
git reset --hard

# if last commit has not been pushed, undo last commit (keep changes, reverts files back to staging)
git reset --soft HEAD~
```

Use `git reset` without `--hard/--soft` to move `HEAD` to point to specified commit *without* changing the files. The following will undo a commit (if not yet pushed), but keep the changes. The head will now point to the previous commit.

```shell
# undo commit but keep changes, point head to previous commit:
git reset HEAD^
```

# Sources

- [git reset](https://git-scm.com/docs/git-reset)
- [git stash](https://git-scm.com/docs/git-stash)