- [Undo Changes](#undo-changes)

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

# Undo Changes
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
