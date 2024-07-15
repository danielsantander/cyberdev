- [Windows](#windows)
  - [SMBv1](#smbv1)
  - [SMB v2/v3](#smb-v2v3)
  - [Sources](#sources)

---

# Windows

## SMBv1

Windows 8 & Windows Server 2012

```shell
# detect status
Get-SmbServerConfiguration | Select EnableSMB1Protocol

# enable SMB protocols
Set-SmbServerConfiguration -EnableSMB1Protocol $false

# disable SMB protocols
Set-SmbServerConfiguration -EnableSMB1Protocol $true
```

> You don't have to restart the computer after you run the Set-SMBServerConfiguration cmdlet.

Windows 7, Windows Server 2008 R2, Windows Vista, or Windows Server 2008 via PowerShell 2.0 or later. SMBv1 on SMB Server:

```shell
# detect
Get-Item HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | ForEach-Object {Get-ItemProperty $_.pspath}

# disable
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 0 -Force

# enable
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 1 -Force
```

> You must restart the computer after you make these changes.

## SMB v2/v3

Windows 8 & Windows Server 2012

```shell
# detect
Get-SmbServerConfiguration | Select EnableSMB2Protocol

# disable
Set-SmbServerConfiguration -EnableSMB2Protocol $false

# enable
Set-SmbServerConfiguration -EnableSMB2Protocol $true
```

Windows 7, Windows Server 2008 R2, Windows Vista, or Windows Server 2008 via PowerShell 2.0 or later.

```shell
# detect
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | ForEach-Object {Get-ItemProperty $_.pspath}

# disable
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB2 -Type DWORD -Value 0 -Force

# enable
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB2 -Type DWORD -Value 1 -Force
```

> You must restart the computer after you make these changes.

## Sources

- [Detect SMBv1/v2](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3?tabs=server)