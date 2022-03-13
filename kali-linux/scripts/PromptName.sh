#! /bin/bash

# script that prompts user for their name and outputs a message

# prompt user for input
echo 'What is your name?'

# save input into variable
read name

# output variable value
# echo 'Welcome' $name '!'
echo "Welcome ${name}!"