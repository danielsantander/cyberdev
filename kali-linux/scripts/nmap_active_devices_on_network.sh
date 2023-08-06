#!/bin/bash

if [ -z "$1" ]
  then
    cidr=$(ip --brief address show | awk '$3 ~ /^[0-9]{1,3}(\.[0-9]{1,3}){3}\/[0-9]{2}$/ {print $3}')
else
    cidr=$1;
fi
echo ""

# Use expansion operator -> ${parameter:+[word]}
#    Uses Alternative Value.
#    If parameter is unset or null, null shall be substituted;
#    otherwise, the expansion of word (or an empty string if word is omitted)
#    shall be substituted.
if [ -z ${cidr+x} ]; then
    echo "No IP address range provided, exiting.";
    exit 1;
else
    echo "performing nmap (sP scan) on $cidr ..."

    network=$(nmap -sP $cidr | awk '$NF ~ /[0-9]+(\.[0-9]+){3}/ {print $NF}')

    if [[ $? -gt 0 ]]; then
        echo -e "\n\nIP RETRIEVAL FAILED\n"
    elif [[ $? -eq 0 || -z $network ]]; then
        echo -e "\nNO IPs FOUND\n";
    else
        echo -e "\n--------------------\nIP ADDRESSES FOUND:\n--------------------";
        echo "$network"
    fi
    echo ""
fi;
