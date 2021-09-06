#!/bin/bash
sudo iwlist wlan0 scanning | egrep -c 'Cell |Encryption|Quality|Last beacon|ESSID'
