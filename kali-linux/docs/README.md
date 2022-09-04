Documentation for linux distributions operating with the Linux kernel. For demonstration purposes I will be referring to the Kali Linux Operation System.

**Table of Contents**
- [Change IP Addresses](./01_change_ip_address.md)
- [Change MAC Addresses](./02_change_MAC_address.md)
- [Assign IP Address](./03_assign_ip_address.md)
- [dig Command](./04_dig_command.md)
- [Change DNS](./05_change_dns_server.md)
- [IP Host Mapping](./06_map_ip_address_w_hosts_file.md)
- [Manage Software](./07_add_remove_software.md)
- [Manage Permissions](./08_permissions.md)
- [Process Management](./09_process_management.md)
- [Environment Variables](./10_env_variables.md)
- [Scripting](./11_scripting.md)
- [Compression](./12_compression.md)
- [Filesystem](./13_filesystem.md)
- [Logging](./14_logging.md)
  - [Log Configuration](./14_logging.md#log-configuration)
  - [Log Rotate](./14_logging.md#logrotate)
  - [Shred files](./14_logging.md#shred-files)
  - [Disable logging](./14_logging.md#disable-logging)

- [Services](./15_services.md)
  - [Manage Services](./15_services.md#manage-services)
  - [Apache Server](./15_services.md#apache-web-server)
  - [OpenSSH](./15_services.md#openssh)
  - [MySQL](./15_services.md#mysql)
  - [PostgreSQL](./15_services.md#postgresql)
- [Anonymity](./16_anonymity.md)
  - [traceroute command](./16_anonymity.md#traceroute)
  - [The Onion Router (Tor)](./16_anonymity.md#the-onion-router-tor)
  - [Proxy Servers](./16_anonymity.md#proxy-servers)
  - [proxychains configurations](./16_anonymity.md#proxychains-configurations)

## Applications:
- [Metasploit](Metasploit.md) - Open source software tool for developing and executing exploit code against a targeted machine.
  - [PostgreSQL](Metasploit.md#postgresql-postgres)
  - [Start Metasploit](Metasploit.md#start-metasploit)
- [MySQL](MySQL.md)
  - [Login](MySQL.md#login)
  - [Databases](MySQL.md#databases)
  - [Tables](MySQL.md#tables)
  - [Table Columns](MySQL.md#table-columns)
  - [Command](MySQL.md#commands)
- [raspistill](raspistill.md) - (Raspberry Pi application)

<hr>

# Tips

## Changing Shell
To change to a specific shell (for example zsh): `chsh -s /bin/zsh`

## Change File Permissions
`chmod` is the command and system call used to change the access permissions and the special mode flags (the setuid, setgid, and sticky flags) of file system objects (files and directories). Collectively these were originally called its modes, and the name chmod was chosen as an abbreviation of change mode. [wiki source](https://en.wikipedia.org/wiki/Chmod)

**Example**
Change script into an executable:  `chmod 755 myscript`

The digits (7,5,5) each individually represent the permissions granted for the user, group, and others, in that order. (Each digit is a combination of the numbers 4,2,1,0
  - 0 is "no permission"
  - 1 is "execute permissions"
  - 2 is "write permissions"
  - 4 is "read permissions"

> The digits `755` represent granting all permissions for the user, and "read/execute permissions" for group & others.

Permission Table Combinations:
Binary|  Dec  | value       |
------|-------|-------------|
0000  |   0   | no permission
0001  |   1   | execute
0010  |   2   | write
0011  |   3   | execute & write
0100  |   4   | read
0101  |   5   | execute & read
0110  |   6   | write & read
0111  |   7   | execute & write & read
