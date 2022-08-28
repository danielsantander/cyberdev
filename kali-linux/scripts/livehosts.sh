#!/bin/bash

# usage: ./livehosts.sh {IP/CIDR}
nmap $1 -n -sP | grep report | awk '{print $5}'