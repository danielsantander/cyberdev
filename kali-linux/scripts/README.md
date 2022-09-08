
*Table of Contents*
- [Install NMAP](#install-nmap)
- [findhiddenfiles.sh](#findhiddenfilessh)
- [HelloWorld](#helloworld)
- [livehosts.sh](#livehostssh)
- [MySQLScan.sh](#mysqlscansh)
- [MySQLScan2.sh](#mysqlscan2sh)

# Install NMAP
```shell
sudo apt install -y nmap
```

# findhiddenfiles.sh
Outputs a list of hidden files found in current directory.

Usage: `./findhiddenfiles.sh`

# HelloWorld
Outputs "Hello World!"

Usage: `./HelloWorld`

# livehosts.sh
Outputs a list of live hosts on given network.

Usage: `./livehosts.sh {IP/CIDR}`

# MySQLScan.sh
Performs `nmap` scan to find hosts with open port 3306.

Usage: `./MySQLScan.sh`

Output Files:
- ResultsMySQLScan
- ResultsOpenMySQLPorts

# MySQLScan2.sh
Advanced version of `MySQLScan.sh` allowing user input.

Usage: `./MySQLScan2.sh`

Input when prompted:
- first ip address
- last octet of the last IP address
- port number