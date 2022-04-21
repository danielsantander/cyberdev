*Table of Contents*
- [Develop Branch](#develop-branch)
- [Branch Types](#branch-types)
  - [Feature Branches](#feature-branches)
    - [Create new feature branch](#create-new-feature-branch)
    - [Merge feature into develop](#merge-feature-into-develop)
  - [Ticket Branches](#ticket-branches)
  - [Release Branches](#release-branches)
    - [Creating release branch](#creating-release-branch)
    - [Merge release into develop](#merge-release-into-develop)

# Develop Branch
Consider `origin/develop` to be the main branch for development source code and where `HEAD` reflects the state with the latest development changes for the next release.

# Branch Types
Different type of branches:
- feature
- ticket
- release

## Feature Branches
Branched from `develop`, merges back into `develop`.

Naming convention: anything other than `develop`,`master`,`ticket-*`, `release-*`

### Create new feature branch
Branch off the develop branch to create a feature branch:
```shell
$ git checkout -b myNewFeature develop
Switched to a new branch "myNewFeature"
```

### Merge feature into develop
Merge the finished feature into the `develop` branch. Use the `--no-ff` flag (no fast forward) to create a new commit object, avoiding losing any information about the historical existence of the feature branch (grouping together all commits creating the feature).

```shell
$ git checkout develop
Switched to branch 'develop'

$ git merge --no-ff myNewFeature
Updating...

$ git branch -d myNewFeature
Deleted branch myNewFeature

$ git push origin develop
```

## Ticket Branches
Similar to feature branches, branches from `develop` branch and merges back into the `develop` branch.

Naming convention: `ticket-<ticket_number>`

Same branching and merging convention as `feature` branch.

## Release Branches
Branches from `develop` and merges back either `develop` or `master`.

Naming convention: `release-<release_number>`

### Creating release branch
```shell
$ git checkout -b release-1.2.3.4 develop
Switched to a new branch "release-1.2.3.4"

$ git commit --allow-empty -m "Start release branch version 1.2.3.4"
```

### Merge release into develop
```shell
$ git checkout develop

$ git merge --no-ff release-1.2.3.4
...

$ git branch -d release-1.2.3.4
Deleted branch release-1.2.3.4
```
