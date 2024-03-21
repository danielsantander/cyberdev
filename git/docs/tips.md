- [List Branches by order](#list-branches-by-order)
- [Update](#update)
- [Move files from one branch into current](#move-files-from-one-branch-into-current)
- [Pull files from another commit](#pull-files-from-another-commit)
- [Ignore already tracked files](#ignore-already-tracked-files)
- [Ignore Untracked Files](#ignore-untracked-files)

# List Branches by order

List **local** branches in order from recent to oldest with the given format:
```shell
$ git for-each-ref --sort=-committerdate refs/heads/ --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'
```

List **remote** branches in order from recent to oldest with the given format:
```shell
$ git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'
```

# Update
Update remote branches:
```shell
$ git remote update origin --prune
```

Update local branches:
```shell
$ git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
```

# Move files from one branch into current

**Example**: Pull files from local branch into the currently checked out branch.
```shell
$ git checkout develop
$ git checkout localBranch .
```

# Pull files from another commit
[From this Answer](https://stackoverflow.com/a/51719585/14745606)

**Example**: move files made from a commit into the currently checked out branch.
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

# Ignore already tracked files
[From this question](https://stackoverflow.com/questions/10755655/git-ignore-tracked-files)

Usage: `git update-index --assume-unchanged [<file> ...]`

Usage to start tracking again: `git update-index --no-assume-unchanged [<file> ...]`

# Ignore Untracked Files

Use `git clean` -- [src](https://stackoverflow.com/a/64966)

```shell
# Print out the list of files and directories which will be removed (dry run)
# where: -n -> dry run and -d -> remove untracked directories
git clean -n -d
```