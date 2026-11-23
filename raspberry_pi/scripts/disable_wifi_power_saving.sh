#!/bin/bash

# DISABLE Wi-Fi Power Saving
# ------------------------------
# By default, Raspberry Pi OS turns off or lowers power to the Wi-Fi chip when it detects inactivity, causing it to drop offline.
# 1. Power-cycle your Pi so you can temporarily SSH back into it.
# 2. Run this command to check if power management is active:
# iwconfig wlan0

# 3. Look for a line that says Power Management:on. If it is on, turn it off temporarily to test:
# sudo iwconfig wlan0 power off

# 4. To make this change permanent so it persists after rebooting, open your interfaces configuration file:
# sudo vi /etc/rc.local

# Add the following line right above the exit 0 line at the bottom:bash
# iwconfig wlan0 power off

# 6. Save and exit

# -----------------------------------------------------------------------
# Automated Script Logic
# -----------------------------------------------------------------------
log (){
    msg=$1
    if [ -n "$msg" ]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] $msg"
    fi
}
POWER_STATUS=$(iwconfig wlan0 2>/dev/null | grep -oP 'Power Management:\s*\K\S+')
if [ "$POWER_STATUS" = "off" ]; then
    log "Power Management is OFF"
    # Add your code here for when it's off
elif [ "$POWER_STATUS" = "on" ]; then
    log "Power Management is ON, turning off temporarily ..."
    sudo iwconfig wlan0 power off
else
    log "Could not determine Power Management status (Value found: $POWER_STATUS)"
fi
