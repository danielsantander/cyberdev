# GIT Tips and Scripts

Notes and tips will be written in markdown files (`.md` extension) while scripts will be written in shell scripts (`.sh` extension).


**View All GIT Settings**

```shell
$ git config --list --show-origin
```

## Set User Info
```shell
$ git config --global user.name "Jane Doe"
$ git config --global user.email janedoe@email.com
```

Use the `--global` option to set so these are set for the whole system, and will only need to be performed once.

Omit this if you are planing to use different user configurations for specific projects.

### Cache User Creds
To have the credentials cached. Prevents enter credentials prompt for the given timeout in seconds. 

Cache credentials for 3 hours (10800 seconds)
```shell
$ git config --global credentials.helper 'cache --timeout=10800'
```

### Store Creds
```shell
$ git config --global credentials.helper store
```
> **WARNING: ** This is not recommended. This will store your credentials in plain text on your machine, making it susceptible for acess from a bad actor.

### Setup SSH
This is the best and prefered way to communicate remotely.
Once you have your SSH keys and add them to your GitHub account settings you can pull and push without a prompt for verifying your credentials.

#### Troubleshooting
If you have already been working in a project where the repository's remote url is for the default
HTTPS url, you will need to update the projcet's `.git/config` file settings.
Within the git project directory, update the remote url with the following command:

We view the config file to see what the remote url is set to:
```shell
root@kali:~/scripts# cat .git/config 
...
[remote "origin"]
        url = https://github.com/<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
...
```

Update the remote url with the following command:
```shell
root@kali:~/scripts# git remote set-url origin git@github.com:<username>/<repository>.git
```

Now we can see it is updated:
```shell
root@kali:~/scripts# cat .git/config 
...
[remote "origin"]
        url = git@github.com:<username>/<repository>.git
        fetch = +refs/heads/*:refs/remotes/origin/*
...
```
