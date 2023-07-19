#! /bin/bash

pwd && echo "";
# get git repo
echo -n 'Enter git repository path: '
read dirpath
cd "${dirpath}"


# delete gone branches
pwd && echo -e "\ndeleting the gone branches...\n";


# git for-each-ref --format '%(refname:short) %(upstream:track)' | awk '$2 == "[gone]" {print $1}' | xargs -r git branch -D
# xargs on Mac OS X doesn't support the --replace (-r) option, use -I instead


# git for-each-ref --format '%(refname:short) %(upstream:track)' | awk '$2 == "[gone]" {print $1}' | xargs -I {} echo 'git branch -D {}' # ECHO OUT FOR TESTING
git fetch -p && git for-each-ref --format '%(refname:short) %(upstream:track)' | awk '$2 == "[gone]" {print $1}' | xargs -I {} git branch -D {}


echo -e "\n\n...finished."
