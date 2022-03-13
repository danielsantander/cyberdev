#! /bin/bash

# Advanced version of MySQLScan.sh allowing user input.

echo "Enter starting IP address:"
read firstIP
echo "Enter last octet of the last IP address:"
read lastOctetIP
echo "Enter port number:"
read port

nmap -sT $firstIP-$lastOctetIP -p $port > /dev/null -oG ResultsMySQLScan2
cat ResultsMySQLScan2 | grep open > ResultsOpenMySQLPorts2
cat ResultsOpenMySQLPorts2