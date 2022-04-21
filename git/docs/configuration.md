
- [Configuration](#configuration)
  - [Set User Info](#set-user-info)
  - [Set Text Editor](#set-text-editor)
  - [Cache User Creds](#cache-user-creds)
  - [Delete Cached Record](#delete-cached-record)
  - [Store Creds](#store-creds)
- [Setup SSH for GitHub](#setup-ssh-for-github)
- [Troubleshooting](#troubleshooting)
  - [Update Remote URL](#update-remote-url)

# Configuration

View all settings
```shell
$ git config --list --show-origin
```

View global configurations
```shell
$ git config --list --global
```

When running config commands, use the `--global` option to apply settings for the whole system (will only need to be performed once),otherwise omit this if you are planing to use different user configurations for specific projects.

## Set User Info
Set username and email
```shell
$ git config --global user.name "Bruce Wayne"
$ git config --global user.email bruce@wayne.ent
```

## Set Text Editor
```shell
$ git config --global core.editor <EDITOR_NAME_HERE>
# Example:
$ git config --global core.editor emacs
```
> Windows systems: need to specify full path to the executable file
> 32-bit Windows system, or 64-bit editor on 64-bit system: may try the following:
> `git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"`

## Cache User Creds
Cash user credentials (prevents enter credentials prompt for the given timeout in seconds). 

The following will cache credentials for 3 hours (10800 seconds):
```shell
$ git config --global credentials.helper 'cache --timeout=10800'
```

## Delete Cached Record
```shell
$ git config --global --unset credential.helper
$ git config --system --unset credential.helper
```

## Store Creds
```shell
$ git config --global credentials.helper store
```
> **WARNING: ** This is not recommended. This will store your credentials in plain text on your machine, making it susceptible for access by a bad actor.

# Setup SSH for GitHub
This is the best and preferred way to communicate remotely.
Once you have your SSH keys and add them to your GitHub account settings you can pull and push without a prompt for verifying your credentials.

# Troubleshooting

## Update Remote URL
If you have already been working in a project where the repository's remote url is for the default
HTTPS url, you will need to update the projcet's `.git/config` file settings.
Within the git project directory, update the remote url with the following command:

View the config file to see what the remote url is set to:
```shell
$ cat .git/config 
...
[remote "origin"]
        url = https://github.com/<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
...
```

Update the remote url with the following command:
```shell
$ git remote set-url origin git@github.com:<username>/<repository>.git
```

Now we can see it is updated:
```shell
$ cat .git/config 
...
[remote "origin"]
        url = git@github.com:<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
...
```
