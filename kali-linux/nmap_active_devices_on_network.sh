#!/bin/bash

ipaddress=$(ip --brief address show | awk '$3 ~ /^[0-9]{1,3}(\.[0-9]{1,3}){3}\/[0-9]{2}$/ {print $3}')
echo "performing nmap on $ipaddress..."

network=$(nmap -sP $ipaddress | awk '$NF ~ /[0-9]+(\.[0-9]+){3}/ {print $NF}')
echo "ip address found: "
echo "$network"
