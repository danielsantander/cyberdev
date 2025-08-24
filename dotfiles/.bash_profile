# set PATH variable, run commands that are needed only once at start of session

alias get_ubuntu_users="awk -F'[/:]' '{if ($3 >= 1000 && $3 != 65534) print $1}' /etc/passwd"; # retrieve users from Ubuntu using ':' as a delimeter, if user ID is larger than 1000 and not 65534 (reserved for 'nobody')

alias djs-date="date +%Y%m%d-%H:%M:%S"
