# Lab 01 – Layer 2 Network Investigation (macOS)

## Overview

This lab investigates how the Data Link Layer (Layer 2) operates on a real macOS computer. The objective is to identify the active Network Interface Card (NIC), examine its MAC address, verify that the interface is operational, and understand how Layer 2 enables communication within a Local Area Network (LAN).

Unlike a simple command demonstration, this lab focuses on interpreting the results and developing the troubleshooting mindset expected of a Network Engineer.


# Objectives

By completing this lab, I was able to:

* Identify the active network interface.
* Locate the MAC address of the active NIC.
* Verify the operational status of the interface.
* Understand the relationship between NICs and MAC addresses.
* Explain why a computer may have multiple NICs.
* Relate Layer 2 concepts to a real network environment.
* Practice structured Layer 2 troubleshooting.



# Lab Environment

| Item             | Details                  |
| ---------------- | ------------------------ |
| Operating System | macOS Ventura            |
| Device           | MacBook Pro 2017         |
| Connection Type  | Wi-Fi                    |
| Active Interface | en0                      |
| Network Type     | Local Area Network (LAN) |



# Background

The Data Link Layer is responsible for local communication within a network.

Every Network Interface Card (NIC) has a unique MAC address that allows switches to identify where frames should be delivered.

This lab investigates these concepts using the built-in networking tools available on macOS.



# Commands Executed

## 1. Display all network interfaces

```bash
ifconfig
```

### Purpose

Displays every network interface available on the computer together with important networking information.

### What I verified

* Available interfaces
* Active interface
* Assigned IP address
* MAC address
* Interface status



## 2. Display hardware ports

```bash
networksetup -listallhardwareports
```

### Purpose

Maps the user-friendly hardware names (such as Wi-Fi) to the underlying interface names (such as en0).

### What I verified

* The Wi-Fi adapter corresponds to interface **en0**.
* The hardware MAC address assigned to the Wi-Fi NIC.



## 3. Inspect the Wi-Fi interface

```bash
ifconfig en0
```

### Purpose

Displays detailed information about the active Wi-Fi interface.

### What I verified

* MAC address
* IPv4 address
* IPv6 address
* Broadcast address
* MTU
* Interface status



## 4. Verify interface status

```bash
ifconfig en0 | grep status
```

### Purpose

Checks whether the network interface is currently operational.

### Expected Result

```text
status: active
```

### Interpretation

The NIC is functioning correctly and is ready to transmit and receive Ethernet/Wi-Fi frames.



# Results

## Active Network Interface

```text
en0
```



## MAC Address

```text
f0:18:98:56:cf:d2
```

This uniquely identifies the Wi-Fi Network Interface Card on the local network.



## IPv4 Address

```text
10.101.143.171
```

This logical address enables communication within the current IP network.



## Interface Status

```text
status: active
```

The Wi-Fi interface is operational.



# Interpretation

The investigation confirms that:

* The MacBook communicates through the Wi-Fi NIC (**en0**).
* The Wi-Fi NIC has its own unique MAC address.
* The interface is active and capable of transmitting Layer 2 frames.
* The computer has successfully joined the local network and received an IP address.



# Layer 2 Concepts Demonstrated

During this lab I confirmed:

* Every NIC has its own MAC address.
* MAC addresses identify the network interface rather than the entire computer.
* The Data Link Layer operates using Ethernet/Wi-Fi frames.
* Switches use MAC addresses to forward traffic within a LAN.
* A working Layer 2 connection is essential before higher OSI layers can communicate.



# Troubleshooting Performed

## Check whether the interface is active

**Command**

```bash
ifconfig en0 | grep status
```

### Healthy Result

```text
status: active
```

### If unsuccessful

Possible causes:

* Wi-Fi disabled
* Driver issue
* Hardware failure
* Airplane mode
* Physical adapter problem



## Verify the MAC Address

**Command**

```bash
ifconfig en0
```

### Healthy Result

A valid MAC address beginning with hexadecimal characters.

### If unsuccessful

Possible causes:

* Incorrect interface selected
* Disabled interface
* Faulty NIC
* Driver problem



## Verify IP Address Assignment

**Command**

```bash
ifconfig en0
```

### Healthy Result

A valid IPv4 address appears.

### If unsuccessful

Possible causes:

* DHCP failure
* Router unavailable
* Cable/Wi-Fi issue
* VLAN misconfiguration
* Incorrect network configuration



# Skills Demonstrated

This lab demonstrates practical experience with:

* Layer 2 networking
* Network Interface Cards (NICs)
* MAC addressing
* Interface verification
* Basic network troubleshooting
* macOS networking tools
* Command-line networking diagnostics



# Reflection  

Before completing this lab, I understood the Data Link Layer mainly from theory.

Performing the investigation on my own computer helped me connect the concepts to a real environment.

I learned that a MAC address belongs to a Network Interface Card rather than the computer itself, understood how to identify active interfaces on macOS, and practised verifying whether a Layer 2 connection is functioning correctly.

This lab also reinforced the importance of troubleshooting methodically by verifying one component at a time instead of making assumptions.


This lab provided practical experience with the core responsibilities of the Data Link Layer. By inspecting a real network interface, verifying its MAC address, and confirming its operational status, I gained hands-on understanding of how Layer 2 enables local network communication and how to troubleshoot common connectivity issues using a structured engineering approach.
