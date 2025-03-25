- [Configuration](#configuration)
  - [Cache User Creds](#cache-user-creds)
  - [Store Creds](#store-creds)
  - [Setup SSH For GitHub](#setup-ssh-for-github)
  - [View Remote URL](#view-remote-url)
  - [Update Remove URL](#update-remove-url)
- [Branching Strategy](#branching-strategy)
  - [Develop Branch](#develop-branch)
  - [Branch Types](#branch-types)
    - [Feature Branches](#feature-branches)
    - [Ticket Branches](#ticket-branches)
    - [Release Branches](#release-branches)
- [Diff](#diff)
  - [diff options](#diff-options)
    - [name status](#name-status)
- [Log](#log)

# Configuration

View settings

```shell
# view all settings
git config --list --show-origin

# view global configurations
git config --list --global

# set username and email
git config --global user.name "Bruce Wayne"
git config --global user.email bruce@wayne.ent

# set text editor
git config --global core.editor <EDITOR_NAME_HERE>
# example:
git config --global core.editor emacs
```

When running config commands, use the `--global` option to apply settings for the whole system (will only need to be performed once),otherwise omit this if you are planing to use different user configurations for specific projects.

> Windows systems: need to specify full path to the executable file
> 32-bit Windows system, or 64-bit editor on 64-bit system: may try the following:
> `git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"`

## Cache User Creds

Cash user credentials (prevents enter credentials prompt for the given timeout in seconds).

```shell
# cache credentials for 3 hours (10800 seconds)
git config --global credentials.helper 'cache --timeout=10800'

# delete Cached Record
git config --global --unset credential.helper
git config --system --unset credential.helper
```

## Store Creds

```shell
git config --global credentials.helper store
```

> **WARNING**: This is not recommended. This will store your credentials in plain text on your machine, making it susceptible for access by a bad actor.

## Setup SSH For GitHub

This is the best and preferred way to communicate remotely.
Once you have your SSH keys and add them to your GitHub account settings you can pull and push without a prompt for verifying your credentials.

## View Remote URL

View the config file to see what the remote url is set to:

```shell
cat .git/config
...
[remote "origin"]
        url = https://github.com/<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
...
```

## Update Remove URL

If you have already been working in a project where the repository's remote url is for the default HTTPS url, you will need to update the project's `.git/config` file settings.

Within the git project directory, update the remote url with the following command:

```shell
git remote set-url origin git@github.com:<username>/<repository>.git

# check to see it is updated:
$ cat .git/config
...
[remote "origin"]
        url = git@github.com:<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
```

# Branching Strategy

## Develop Branch

The intention of this branch is to have an exact copy of production in the repository. Consider `origin/develop` to be the main branch for development source code and where `HEAD` reflects the state with the latest development changes for the next release.

## Branch Types

Different type of branches:

- feature
- ticket
- release

### Feature Branches

Branched from `develop`, merges back into `develop`.

Naming convention: `develop`,`master`,`ticket-*`, `release-*`

Create a new feature branch

```shell
# branch off the develop branch to create a feature branch
git checkout -b myNewFeature develop
Switched to a new branch "myNewFeature"

git commit --allow-empty -m "start new branch for my new feature"

git push -u origin myNewFeature
```

Merge feature branch into develop branch, use `--no-ff` flag (no fast forward) to create a new commit object, avoiding losing any information about the historical existence of the feature branch (grouping together all commits creating the feature).

```shell
# position at develop branch
git checkout develop

# merge feature branch (use --no-ff param)
git merge --no-ff myNewFeature

# delete the feature branch locally
git branch -d myNewFeature

# delete the feature branch in the remote
git push -d origin myNewFeature

# push changes to the shared repo
git push origin develop
```

### Ticket Branches

Similar to feature branches, ticket branches branch from and merge back into the `develop` branch.

Naming convention: `ticket-<ticket_number>`

Same branching and merging convention as `feature` branch.

### Release Branches

Branches from `develop` and merges back into either `develop` or `master`.

Naming convention: `release-<release_number>`

Creating new release branch example: `git checkout -b release-1.2.3.4`

Same branching and merging convention as `feature` branch.

# Diff

The `diff` command runs a diff function on Git data sources such as: commits, branches, files, etc.

## diff options

### name status

Show names and status of changed files.

Usage: `git diff --name-status`

```shell
# Use the diff command to show all changed files on a given branch.
git diff --name-status branch_name

# use the same command but pipe with grep go search for changed files named "testFiles"
git diff --name-status branch_name | grep "testFile[s]"
```

# Log

```shell
# list all commits for specific filepath -- a path which can be either a file and/or directory
git log --follow <filepath>

# list all commits for README.md file
git log --oneline --follow git/docs/README.md

# display commits that develop branch has but main branch does not.
git log main..develop --oneline
```
