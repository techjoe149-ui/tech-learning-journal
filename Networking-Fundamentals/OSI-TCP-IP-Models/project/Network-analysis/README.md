# Project – Layer 2 Network Analysis

## Project Overview

This project applies the concepts learned in the Data Link Layer by analyzing my own home network from a Layer 2 perspective.

Instead of only running networking commands, the objective is to explain how communication occurs within my Local Area Network (LAN), identify the devices involved, understand how frames are forwarded, and demonstrate the troubleshooting process a Network Engineer would follow when Layer 2 issues occur.



# Project Objectives

By completing this project, I aimed to:

* Identify the active Network Interface Card (NIC).
* Determine the MAC address of the active interface.
* Explain how Layer 2 communication occurs within my LAN.
* Explain the roles of the NIC, switch, router and ARP.
* Demonstrate an understanding of Ethernet frames.
* Apply Layer 2 troubleshooting techniques.
* Produce professional documentation suitable for a technical portfolio.



# Network Environment

| Component        | Description      |
| ---------------- | ---------------- |
| Computer         | MacBook Pro 2017 |
| Operating System | macOS Ventura    |
| Active Interface | Wi-Fi (en0)      |
| Connection Type  | Wireless LAN     |
| IP Address       | 10.101.143.171   |
| MAC Address      | f0:18:98:56:cf   |



# Network Topology

```text
                 Internet
                     │
                     │
               ISP Network
                     │
                     │
             Wireless Router
                     │
      ┌──────────────┼──────────────┐
      │              │              │
   Laptop         Smartphone      Printer
   (en0)                            (Optional)
```

Although the connection between my laptop and the router is wireless, Layer 2 communication still relies on MAC addresses.



# How Communication Happens

## Scenario 1 – Communicating with Another Device on the Same LAN

Suppose my laptop wants to send data to another device connected to the same Wi-Fi network.

The communication process is:

1. The application creates data.
2. The Network Layer determines that the destination is on the same local network.
3. If the destination MAC address is unknown, the laptop sends an ARP Request asking:

   > "Who has this IP address?"
4. The destination device replies with its MAC address.
5. My laptop stores the mapping in its ARP cache.
6. The NIC creates an Ethernet frame containing:

   * Source MAC
   * Destination MAC
7. The frame is transmitted to the wireless router/access point.
8. The switching function forwards the frame only to the correct destination.

No routing is required because both devices are on the same LAN.



## Scenario 2 – Accessing the Internet

When opening a website:

1. My laptop determines that the destination is outside the local network.
2. It sends an ARP request for the default gateway if necessary.
3. The router's MAC address is learned.
4. The Ethernet frame is addressed to the router.
5. The router removes the Layer 2 information, examines the IP packet, and forwards it toward the destination network.

In this case, the router becomes necessary because communication leaves the local network.



# Layer 2 Components Identified

## Network Interface Card (NIC)

The active NIC is:

```text
en0
```

Responsibilities:

* Connects the computer to the network.
* Possesses a unique MAC address.
* Sends and receives Layer 2 frames.



## MAC Address

```text
f0:18:98:56:cf:d2
```

This identifies the Wi-Fi NIC on the local network.

A MAC address identifies the network interface, not the entire computer.



## Ethernet Frame

Every Layer 2 transmission is encapsulated inside an Ethernet frame containing:

* Destination MAC Address
* Source MAC Address
* Payload
* Frame Check Sequence (FCS)

These fields allow switches to deliver frames accurately and detect transmission errors.


## ARP

ARP allows communication between Layer 3 and Layer 2.

It resolves an IP address into the destination MAC address before a frame is transmitted.

Without ARP, devices would know the destination IP address but would not know which MAC address should receive the Ethernet frame.



# Layer 2 Troubleshooting Workflow

When investigating Layer 2 problems, I would follow this sequence:

### Step 1 – Verify the Network Interface

Command:

```bash
ifconfig en0
```

Expected result:

* Interface exists.
* Interface is active.
* Valid MAC address displayed.



### Step 2 – Verify Interface Status

Command:

```bash
ifconfig en0 | grep status
```

Healthy result:

```text
status: active
```

If inactive:

* Enable Wi-Fi.
* Check hardware.
* Restart the interface.
* Restart the computer if necessary.

---

### Step 3 – Verify IP Address

Command:

```bash
ifconfig en0
```

Expected:

A valid IPv4 address.

Possible failures:

* DHCP failure.
* Router unavailable.
* VLAN issue.
* Incorrect network settings.



### Step 4 – Verify ARP Resolution

Command:

```bash
arp -a
```

Expected:

Entries showing IP-to-MAC mappings for devices that have recently communicated with the computer.

If the required device is missing:

* Ping the destination.
* Recheck the ARP cache.
* Verify the destination device is powered on and connected.



### Step 5 – Test Connectivity

Command:

```bash
ping <destination IP>
```

Expected:

Successful replies.

If unsuccessful:

* Confirm the destination device is online.
* Check Wi-Fi signal quality.
* Verify both devices are on the same network.
* Check for VLAN separation.
* Verify the router or switch configuration if applicable.



# Skills Demonstrated

This project demonstrates practical understanding of:

* Layer 2 networking
* Ethernet communication
* MAC addressing
* Network Interface Cards
* ARP
* Switching concepts
* Basic network troubleshooting
* Network documentation
* Technical reporting



# Reflection

Completing this project helped me connect theoretical networking concepts with a real environment.

 I investigated my own network, identified the active interface, interpreted networking information, and developed a structured troubleshooting process. I also gained a clearer understanding of the relationship between NICs, MAC addresses, Ethernet frames, ARP, switches, and routers.

This project reinforced the importance of thinking like a Network Engineer by validating assumptions with evidence before attempting to solve a networking problem.




# Conclusion

This project demonstrates my ability to analyze a real Layer 2 network, explain how local communication occurs, and apply a structured troubleshooting methodology. It provides practical evidence of my understanding of the Data Link Layer and forms part of my Networking Fundamentals learning portfolio.
