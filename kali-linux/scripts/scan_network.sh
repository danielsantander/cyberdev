#!/bin/bash

# requires nmap
if [ -z $1 ]; then
    echo "No IP address range provided, exiting."
    exit 1
fi

# verify ip address/subnet
REGEX_IP='^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(\/[0-9]+)?$'
if [[ $1 =~ ${REGEX_IP} ]]; then
    cidr=$1
else
    echo "invalid ip address/subnet"
    exit 1
fi

echo "performing nmap (sP scan) on $cidr ..."
network=$(nmap -sP $cidr | awk '$NF ~ /[0-9]+(\.[0-9]+)*/ {print $NF}')

# todo:
    # - add different type of scans as options
        # - perform `nmap -sT -Pn IP_ADDR` type scan as option

if [[ $? -gt 0 ]]; then
    echo -e "\n\nIP RETRIEVAL FAILED\n"
elif [[ $? -eq 0 || -z $network ]]; then
    echo -e "\nNO IPs FOUND\n"
else
    echo -e "\n--------------------\nIP ADDRESSES FOUND:\n--------------------"
    echo "$network"
fi
exit 0
