# set PATH variable, run commands that are needed only once at start of session

alias cyberdev--get-ubuntu-users="awk -F'[/:]' '{if ($3 >= 1000 && $3 != 65534) print $1}' /etc/passwd"; # retrieve users from Ubuntu using ':' as a delimeter, if user ID is larger than 1000 and not 65534 (reserved for 'nobody')

alias cyberdev--date="date +%Y%m%d-%H:%M:%S"
