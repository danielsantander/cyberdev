#!/bin/bash

if [ -z "$1" ]
  then
    ip_address_range=$(ip --brief address show | awk '$3 ~ /^[0-9]{1,3}(\.[0-9]{1,3}){3}\/[0-9]{2}$/ {print $3}')
else
    ip_address_range=$1;
fi

# Use expansion operator -> ${parameter:+[word]}
#    Uses Alternative Value. 
#    If parameter is unset or null, null shall be substituted;
#    otherwise, the expansion of word (or an empty string if word is omitted)
#    shall be substituted.
if [ -z ${ip_address_range+x} ]
then
    echo "ip address range ($ip_address_range) is unset, exiting.";
    exit 1;
else
    echo "performing nmap on $ip_address_range ..."

    network=$(nmap -sP $ip_address_range | awk '$NF ~ /[0-9]+(\.[0-9]+){3}/ {print $NF}')
    echo "IP addresses found: "
    echo "$network"
fi;
