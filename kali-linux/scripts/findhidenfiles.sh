#!/bin/bash

#TODO: provide some options the user can pass in
# - specified search path
# - file extension

# usage: ./findhiddenfiles.sh
find . -type f -name '.*'

# find all .sh files:
# find . -type f -name '*.sh'