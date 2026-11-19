# Commands Used — Lab 1: Network Inspection (macOS)

## 1. Display the Computer Hostname

```bash
hostname


### Purpose

Displays the computer's hostname (network name).

### What I Learned

The hostname uniquely identifies my computer on the local network and is 
useful for identifying devices

## 2. List All Network Interfaces

```bash
networksetup -listallhardwareports
```

### Purpose

Displays all hardware network ports and their associated device names.

### What I Learned

I identified my Wi-Fi interface (e.g., `en0`), Ethernet interface , Bluetooth interface, and other network adapters such as 
Thunderbolt Bridge.



## 3. Display My Private IP Address

```bash
ipconfig getifaddr en0
```

### Purpose

Displays the IPv4 address assigned to the specified network interface.

### What I Learned

I identified my computer's private IP address used within my local 
network.



## 4. Find the Default Gateway (Router)

```bash
netstat -rn | grep default
```

### Purpose

Displays the default route used to send traffic outside the local network.

### What I Learned

I identified my router's IP address, also known as the default gateway.



## 5. Display DNS Servers

```bash
scutil --dns | grep "nameserver"
```

### Purpose

Lists the DNS servers currently configured on the system.

### What I Learned

I discovered which DNS servers translate domain names into IP addresses.



## 6. Display the MAC Address

```bash
ifconfig en0
```

### Purpose

Displays detailed information about the selected network interface.

### What I Learned

I located my network interface's MAC (Ethernet) address and viewed 
additional interface information.



## 7. Display the Public IP Address

```bash
curl ifconfig.me
```

### Purpose

Queries an online service to display my network's public IP address.

### What I Learned

I identified the public IP address assigned to my Internet connection.



## 8. Test Connectivity with Ping

```bash
ping google.com
```

### Purpose

Tests network connectivity by sending ICMP Echo Requests to a remote host.

### What I Learned

I verified that my computer could communicate successfully with Google's 
servers and measured basic network responsiveness.



## 9. Display the Route to a Remote Host

```bash
traceroute google.com
```

### Purpose

Shows the path packets take from my computer to Google's servers.

### What I Learned

I observed the routers (hops) that my network traffic passes through 
before reaching its destination.



# Summary

Through these commands I learned how to:

* Identify my computer on a network.
* Inspect available network interfaces.
* Determine my private and public IP addresses.
* Identify my default gateway.
* View configured DNS servers.
* Find my MAC address.
* Test network connectivity.
* Observe the route traffic takes across the Internet.


