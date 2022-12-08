*Table of Contents*
- [Develop Branch](#develop-branch)
- [Branch Types](#branch-types)
  - [Feature Branches](#feature-branches)
    - [Create new feature branch](#create-new-feature-branch)
    - [Merge feature into develop](#merge-feature-into-develop)
  - [Ticket Branches](#ticket-branches)
  - [Release Branches](#release-branches)

# Develop Branch
The intention of this branch is to have an exact copy of production in the repository. Consider `origin/develop` to be the main branch for development source code and where `HEAD` reflects the state with the latest development changes for the next release.

# Branch Types
Different type of branches:
- feature
- ticket
- release

## Feature Branches
Branched from `develop`, merges back into `develop`.

Naming convention: `develop`,`master`,`ticket-*`, `release-*`

### Create new feature branch
Branch off the develop branch to create a feature branch:
```shell
$ git checkout -b myNewFeature develop
Switched to a new branch "myNewFeature"

$ git commit --allow-empty -m "start new branch for my new feature"

$ git push -u origin myNewFeature
```

### Merge feature into develop
Merge the finished feature into the `develop` branch. Use the `--no-ff` flag (no fast forward) to create a new commit object, avoiding losing any information about the historical existence of the feature branch (grouping together all commits creating the feature).

```shell

# position at develop branch
$ git checkout develop

# merge feature branch (use --no-ff param)
$ git merge --no-ff myNewFeature

# delete the feature branch locally
$ git branch -d myNewFeature

# delete the feature branch in the remote
$ git push -d origin myNewFeature

# push changes to the shared repo
$ git push origin develop
```

## Ticket Branches
Similar to feature branches, branches from `develop` branch and merges back into the `develop` branch.

Naming convention: `ticket-<ticket_number>`

Same branching and merging convention as `feature` branch.

## Release Branches
Branches from `develop` and merges back either `develop` or `master`.

Naming convention: `release-<release_number>`

Creating new release branch example: `git checkout -b release-1.2.3.4`

Same branching and merging convention as `feature` branch.
