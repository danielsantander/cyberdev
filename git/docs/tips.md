- [List Branches by order](#list-branches-by-order)
- [Update](#update)

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
