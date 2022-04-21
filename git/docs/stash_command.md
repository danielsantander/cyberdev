Stash changes made to the working copy while having the ability to come back to "re-apply" those changes later.

Usage: `git stash`

# Stash options

## save
Stash changes and save with message.

Usage: `git stash save -m "<message>"`


## list
List stash files

Usage: `git stash list`


## pop
Apply the latest stashed changes into the working directory, and remove them from the stash list.

Usage: `git stash pop`

Usage for specific stash: `git stash pop <stash_name>


## apply
Apply the latest stashed changes into the working directory, and keep them in the stash list.

Usage: `git stash apply`

Usage for specific stash: `git stash apply <stash_name>`

**Example**: apply a specific stash
```shell
$ git stash apply stash@{2}
```

## drop
Remove specific stashes

Usage: `git stash drop <stash_name>`


## clean
Remove all stashes

Usage: `git stash clean`