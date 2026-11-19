# Lesson 4 – Data Link Layer (Layer 2)

## Learning Objectives

By the end of this lesson, I should be able to:

* Explain the purpose of the Data Link Layer.
* Explain why Layer 2 exists and why it is necessary.
* Describe the responsibilities of the Data Link Layer.
* Explain what a Network Interface Card (NIC) is and why a computer can have multiple NICs.
* Explain what a MAC address is and how it differs from an IP address.
* Describe the structure of an Ethernet frame.
* Explain how switches forward frames.
* Understand how a switch learns MAC addresses using the CAM table.
* Explain unicast, broadcast and multicast communication.
* Explain how ARP resolves IP addresses into MAC addresses.
* Differentiate between the ARP cache and the switch's CAM table.
* Explain why routers are sometimes involved and sometimes not.
* Explain why VLANs exist and how they improve security and performance.
* Explain access ports and trunk ports.
* Perform basic Layer 2 troubleshooting using a structured engineer's approach.



# What is the Data Link Layer?

The Data Link Layer is **Layer 2** of the OSI Model.

Its primary responsibility is **local network communication**.

While the Physical Layer is responsible for transmitting raw bits over a medium, the Data Link Layer ensures that those bits are organized into frames and delivered to the correct device on the same local network.

In simple terms:

* Physical Layer moves bits.
* Data Link Layer decides which local device should receive those bits.



# Why Does the Data Link Layer Exist?

Imagine several computers connected to the same switch.

If one computer sends data, every connected device receives the electrical signal.

Without Layer 2 there would be no way of knowing which device should actually process the information.

The Data Link Layer solves this problem by introducing **physical addressing** using **MAC addresses** and packaging data into **Ethernet frames**.



# Main Responsibilities of the Data Link Layer

The Data Link Layer is responsible for:

* Physical (MAC) addressing
* Framing
* Local delivery of data
* Error detection using Frame Check Sequence (FCS)
* Media access control
* Communication with switches
* Supporting VLANs
* Local network troubleshooting



# Network Interface Cards (NICs)

## What is a NIC?

A Network Interface Card (NIC) is the hardware that allows a device to connect to a network.

Without a NIC, a computer cannot communicate over Ethernet or Wi-Fi.

The NIC acts as the bridge between the computer and the physical network.



## Why Can One Computer Have Multiple NICs?

A computer can contain several independent network interfaces.

Examples include:

* Wi-Fi adapter
* Ethernet adapter
* Bluetooth adapter
* USB Ethernet adapter
* Virtual adapters created by virtualization software or VPN software

Each NIC performs a different networking role.



## MAC Addresses

Every NIC has its own MAC address.

Therefore:

One computer

↓

Can have several NICs

↓

Each NIC has its own MAC address.

A MAC address identifies the **network interface**, not the entire computer.



# MAC Address

A MAC (Media Access Control) address is a unique hardware identifier assigned to a network interface.

Example:

```
F0:18:98:56:CF:D2
```

The first part identifies the manufacturer (OUI).

The remaining part uniquely identifies that network interface.



## MAC Address vs IP Address

| MAC Address                          | IP Address                                          |
|                                      |
| Layer 2                              | Layer 3                                             |
| Identifies a NIC                     | Identifies a device's logical location on a network |
| Used inside the local network        | Used between networks                               |
| Usually assigned by the manufacturer | Usually assigned by DHCP or manually                |



# Ethernet Frames

The Data Link Layer packages data into **Ethernet Frames**.

A simplified frame contains:

* Destination MAC Address
* Source MAC Address
* Payload
* Frame Check Sequence (FCS)

The FCS helps detect whether the frame became corrupted during transmission.



# Switches

A switch connects devices within a Local Area Network.

Its job is to forward Ethernet frames to the correct destination.

Unlike a hub, a switch learns which MAC addresses are connected to each of its ports.



# CAM Table

The CAM (Content Addressable Memory) table stores:

```
MAC Address → Switch Port
```

Example:

```
F0:18:98:56:CF:D2 → Port 5
```

This allows the switch to forward frames efficiently instead of sending them to every device.


# Unknown Unicast Flooding

When a switch receives a frame for a MAC address that is not yet in its CAM table, it temporarily floods the frame to all ports except the incoming port.

Once the destination replies, the switch learns the correct MAC-to-port mapping.

Future traffic becomes unicast.

Flooding is therefore a temporary learning mechanism rather than the switch's normal operating mode.



# Types of Layer 2 Communication

## Unicast

One sender → One receiver.

This is the normal communication mode after the switch has learned the destination MAC address.



## Broadcast

One sender → Every device in the same broadcast domain.

Example:

ARP Requests.



## Multicast

One sender → A selected group of devices.

Only devices that belong to the multicast group process the traffic.


# Address Resolution Protocol (ARP)

ARP exists because communication inside a LAN requires MAC addresses.

Applications usually know only the destination IP address.

ARP resolves:

```
IP Address

↓

MAC Address
```

Example:

"Who has 192.168.1.10?"

Only the owner of that IP address replies with its MAC address.



# ARP Cache

Each computer stores recently learned IP-to-MAC mappings in its ARP cache.

This prevents unnecessary ARP broadcasts for every communication.

# CAM Table vs ARP Cache

These two tables serve different purposes.

### CAM Table

Stored inside the switch.

Contains:

```
MAC Address → Switch Port
```

Purpose:

Forward Ethernet frames.



### ARP Cache

Stored inside each computer.

Contains:

```
IP Address → MAC Address
```

Purpose:

Resolve Layer 3 addresses into Layer 2 addresses before communication.


# When Is a Router Needed?

If two devices are on the same local network:

* ARP resolves the destination MAC address.
* The switch forwards the frame.
* No router is required.

If the destination is on another network:

* ARP resolves the MAC address of the default gateway (router).
* The frame is sent to the router.
* The router forwards the packet toward the destination network.



# VLANs (Virtual Local Area Networks)

A VLAN logically separates devices into different broadcast domains while allowing them to use the same physical switch infrastructure.

Benefits include:

* Reduced broadcast traffic
* Better security
* Easier management
* Department isolation
* Improved scalability

Example:

* VLAN 10 – Finance
* VLAN 20 – Human Resources
* VLAN 30 – ICT
* VLAN 40 – CCTV
* VLAN 50 – Guest Wi-Fi



# Access Ports

An access port belongs to one VLAN only.

It normally connects to end devices such as:

* Computers
* Printers
* IP Phones

The connected device does not need to understand VLANs.

The switch already knows which VLAN that port belongs to.


# Trunk Ports

A trunk port carries traffic for multiple VLANs between networking devices.

Typically trunk ports connect:

* Switch ↔ Switch
* Switch ↔ Router
* Switch ↔ Wireless Access Point
The switch temporarily adds IEEE 802.1Q VLAN tags while frames travel across the trunk.

Before sending frames to an end device connected to an access port, the VLAN tag is removed.



# Layer 2 Troubleshooting Mindset

Rather than guessing, I prefer to troubleshoot systematically.

Questions to ask include:

* Is the network cable connected?
* Is the NIC active?
* Does the device have a valid IP address?
* Is the destination on the same network?
* Does the ARP cache contain the correct MAC address?
* Is the switch forwarding frames correctly?
* Is the destination device online?
* Is the correct VLAN assigned?
* Is the switch port configured correctly?
* Is the trunk carrying the required VLAN?

Always verify each layer before moving to the next.



# Commands Practiced

During this lesson I used macOS Terminal to inspect Layer 2 information.

Examples include:

```bash
ifconfig

ifconfig en0

networksetup -listallhardwareports

arp -a

ping

netstat -rn
```

These commands helped verify:

* Network interfaces
* MAC addresses
* Interface status
* ARP cache
* Connectivity
* Routing information



# Career Relevance

Knowledge of the Data Link Layer is essential for roles such as:

* Network Technician
* Network Engineer
* Systems Administrator
* Infrastructure Engineer
* Cloud Engineer
* Cybersecurity Analyst
* SOC Analyst
* Penetration Tester

 I realised these professionals regularly troubleshoot MAC addressing, switching, VLANs, ARP, and local network communication.


# Key Takeaways

* The Data Link Layer is responsible for communication within the local network.
* Every NIC has its own unique MAC address.
* MAC addresses identify network interfaces, not entire computers.
* Switches learn MAC addresses using the CAM table.
* ARP converts IP addresses into MAC addresses for local communication.
* The ARP cache and CAM table are different and serve different purposes.
* Routers are required only when communication leaves the local network.
* VLANs logically separate departments without requiring separate physical switches.
* Access ports carry one VLAN; trunk ports carry multiple VLANs using IEEE 802.1Q tagging.
* Effective troubleshooting follows a structured, layer-by-layer process rather than guesswork.
