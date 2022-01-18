#!/bin/bash
#sudo iwlist wlan0 scan | egrep -c 'Cell |Encryption|Quality|Last beacon|ESSID'
sudo iwlist wlan0 scanning | egrep -c 'Cell |Encryption|Quality|Last beacon|ESSID'
