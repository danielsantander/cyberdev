#!/bin/bash
scan iwlist wlan0 scanning | egrep -c 'Cell |Encryption|Quality|Last beacon|ESSID'
