
*Table of Contents*

- [helloworld](#helloworld)
- [nmap\_active\_devices\_on\_network.sh](#nmap_active_devices_on_networksh)
- [MySQLScan.sh](#mysqlscansh)
- [gitgone.sh](#gitgonesh)
- [livehosts.sh](#livehostssh)
- [scan\_wireless\_access\_points.sh](#scan_wireless_access_pointssh)

---

# helloworld

Test script which will display IP address.

Usage:

```shell
./helloworld [options]
```

| option    | description               |
|-----------|---------------------------|
| date      | output date and datetimes |
| args      | print default args        |

# nmap_active_devices_on_network.sh

Performs nmap (`sP`) to detect and list hosts found.

Usage: `./nmap_active_devices_on_network.sh {IP/CIDR}`

# MySQLScan.sh

Perform scan to find hosts with open port 3306.

Usage: `./MySQLScan.sh`

Output Files:

- ResultsMySQLScan
- ResultsOpenMySQLPorts

Input when prompted:

- first ip address
- last octet of the last IP address
- port number

# gitgone.sh

Removes 'gone' branches from a given git repository. Will prompt for directory of git repository.

Usage: `./gitgone.sh`

# livehosts.sh

Outputs a list of live hosts on given network, utilizing nmap with: `nmap -n -sP`

Usage: `./livehosts.sh {IP/CIDR}`

# scan_wireless_access_points.sh

Utilizes `iwlist wlan0` to list wireless access points.
