#! /bin/bash

# Find hosts with MySQL installed (open port 3306) and output to file.
# Perform TCP scan on the local area network (LAN) with open port 3306
# For stealth, send output to /dev/null
# Send "grepable output" (-oG) to a file named ResultsMySQLScan
    # Grepable output consists of comments (lines starting with a pound (#)) and target lines. 
    # A target line includes a combination of six labeled fields, separated by tabs and followed with a colon.
    # The fields are Host, Ports, Protocols, Ignored State, OS, Seq Index, IP ID, and Status.

# NOTE: 
    # -oG is deprecated.
    # XML output format is far more powerful: -oX filespec (XML output)

nmap -sT 192.168.0.0/24 -p 3306 > /dev/null -oG ResultsMySQLScan

# Display the results by piping the output with grep to filter for lines that include the keyword "open", and save those results into another file.
cat ResultsMySQLScan | grep open > ResultsOpenMySQLPorts

# Display results of the assets with open port 3306
cat ResultsOpenMySQLPorts

# OUTPUT: 
# Host: 192.168.0.69 ()	Ports: 3306/open/tcp//mysql///