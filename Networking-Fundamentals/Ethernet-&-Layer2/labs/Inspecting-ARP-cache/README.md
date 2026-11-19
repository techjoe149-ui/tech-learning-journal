
# Lab 02 — ARP Cache Inspection

**File:** `lab-02-arp-cache/README.md`


## Objective

Inspect the system's ARP cache and identify IPv4-to-MAC address mappings on the local network.

## Environment

- Operating System: macOS
- Active interface: `en0`
- Local IPv4 address: `192.168.100.21`
- Network: `192.168.100.0/24`

## Command Used 


arp -a


Observations

The ARP cache contained an entry for the local gateway:

192.168.100.1 → 2c:0b:ab:83:ac:31

This represents an IPv4-to-MAC mapping.

Another entry appeared as:

169.254.169.254 → incomplete

The incomplete state indicated that the system had not successfully resolved a MAC address for that IPv4 address through ARP.

ARP Relationship

ARP allows a device to determine the MAC address associated with an IPv4 address on the local network.

Conceptually:

IPv4 address → MAC address

Example:

192.168.100.1
      ↓
2c:0b:ab:83:ac:31
Result

Successfully inspected the local ARP cache and identified both a successful mapping and an incomplete ARP entry.

Lessons Learned
ARP operates on the local network.
ARP resolves IPv4 addresses to MAC address 
The ARP cache stores learned mappings.
An incomplete entry indicates that resolution has not successfully produced a MAC address.
The ARP cache is different from a switch's MAC/CAM table.