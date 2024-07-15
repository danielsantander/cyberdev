check_services() {
    if [ -f /etc/services ]; then

        cat /etc/services

        # todo: grep appropriate services:
        # grep -w '80/tcp' /etc/services
        # grep -w '443/tcp' /etc/services
        # grep -E -w '22/(tcp|udp)' /etc/services

    fi
}

scan_subnet() {
    # requires nmap
    if [ -z $1 ]; then
        echo "No IP address range provided, exiting.";
        return;
    fi

    # verify ip address/subnet
    REGEX_IP='^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(\/[0-9]+)?$'
    if [[ $1 =~ ${REGEX_IP} ]]; then
        cidr=$1;
    else
        echo "invalid ip address/subnet";
        return;
    fi

    echo "performing nmap (sP scan) on $cidr ...";
    network=$(nmap -sP $cidr | awk '$NF ~ /[0-9]+(\.[0-9]+)*/ {print $NF}');
    if [[ $? -gt 0 ]]; then
        echo -e "\n\nIP RETRIEVAL FAILED\n";
    elif [[ $? -eq 0 || -z $network ]]; then
        echo -e "\nNO IPs FOUND\n";
    else
        echo -e "\n--------------------\nIP ADDRESSES FOUND:\n--------------------";
        echo "$network";
    fi
}
