# Scripts

## hackdiablo

A script designed for network scanning and monitoring.

- Perform ARP and NMAP scans to discover hosts on the network.
- Retrieve local and public IP addresses.
- Monitor network traffic for a specified duration.
- Enable Raspberry Pi-specific features.
- Quick host discovery.

Ensure you have the necessary permissions to run network scans (e.g., `sudo` for ARP and NMAP scans).

Use the `-v` flag for verbose output.

```bash
# Perform basic host discovery scan (nmap -sn)
python3 hackdiablo.py hostdiscovery -v

# Perform ARP and NMAP scans
sudo python3 hackdiablo.py scan -v

# Specify a subnet to scan:
sudo python3 hackdiablo.py scan 192.168.0/16 -v

# Retrieve hostname, local IP, and public IP:
python3 hackdiablo.py getip

# Retrieve additional information for a specific public IP:
python3 hackdiablo.py getip {public_ip_address}

# Example packet monitor usage:
# outputs packet data to console and saves pcap data to output directory
python3 hackdiablo.py monitor -t 120 -o /path/to/output/dir
sudo python3 hackdiablo.py monitor 20 -o ./data/
```
