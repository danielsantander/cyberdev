# Git Tips

## `git pull`
The `git pull` command is used to fetch and download content from a remote repository and immediately update the local repository to match that content. The `git pull` command is a combination of `git fetch` & `git merge`.

- `git fetch` will download the content from the remote repository.
- `git merge` will merge the content to your local repository, once the content is downloaded. A new merge commit will be created and HEAD updated to point at the new commit.

```shell
$ git pull 
```

## `git pull origin master`
Fetches a copy of the master branch from the original repository, and merges it with the current branch that you have checked out.
```shell
$ git pull origin master
```

## status
Displays paths that have differences between the index file and the current HEAD commit, paths that have differences between the working tree and the index file, and paths in the working tree that are not tracked by Git

```shell
$ git status
```

Use `-uall` option to show individual files in untracked directories
```shell
$ git status -uall
```

Use `--ignored` option to get all show ignored files.
```shell
$ git status --ignored
```

Combine the above two options to  get a list of all the files missing in your repo.
```shell
$ git status -uall --ignored
```

## diff
Command that runs a diff function on Git data sources such as: commits, branches, files and more.

Use the `--name-status` option to show only names and status of changed files. 
```
$ git diff --name-status <branch>
```

## List Branches by order

List **local** branches in order from recent to oldest with the given format:
```shell
$ git for-each-ref --sort=-committerdate refs/heads/ --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'
```

List **remote** branches in order from recent to oldest with the given format:
```shell
$ git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(HEAD) %(color:yellow)%(committerdate) %(color:reset)%(refname:short) %(color:red)%(authorname)'
```

## Update
Update remote branches:
```shell
$ git remote update origin --prune
```

Update local branches:
```shell
$ git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
```
