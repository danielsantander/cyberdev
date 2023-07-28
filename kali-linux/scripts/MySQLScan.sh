#! /bin/bash

echo "Enter starting IP address:"
read firstIP
echo "Enter last octet of the last IP address:"
read lastOctetIP
echo "Enter port number:"
read port

nmap -sT $firstIP-$lastOctetIP -p $port > /dev/null -oG ResultsMySQLScan
cat ResultsMySQLScan | grep open > ResultsOpenMySQLPorts
cat ResultsOpenMySQLPorts