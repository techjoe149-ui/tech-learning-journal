# Lab 01 — Network Interface Inspection

## Objective

Inspect the network interfaces on macOS and identify the active network interface, its MAC address, IPv4 address, and link status.

## Environment

- Operating System: macOS
- Interface inspected: `en0`
- Network connection: Wi-Fi
- Terminal: macOS Terminal

## Commands Used

ifconfig


Observations

The ifconfig output showed several interfaces.

The active Wi-Fi interface was:

en0

The interface had:

MAC address: f0:18:98:56:cf:d2
IPv4 address: 192.168.100.21
Status: active

networksetup -listallhardwareports confirmed that:

Hardware Port: Wi-Fi
Device: en0


Successfully identified the active network interface and its associated MAC address, IPv4 address, and status.

Lessons Learned

A network interface provides a device's connection to a network.
en0 is the active Wi-Fi interface on this Mac.
MAC and IPv4 addresses serve different networking purposes.
ifconfig provides detailed interface information.
networksetup can identify the relationship between macOS hardware ports and interfaces.