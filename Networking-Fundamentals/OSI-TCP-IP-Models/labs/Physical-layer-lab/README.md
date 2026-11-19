# Lab 01 — Physical Layer Investigation (macOS)

## Phase
Phase 2 — OSI Model & TCP/IP Model

## Lesson Reference
Lesson 3 — Physical Layer (Layer 1)


# Objective

The purpose of this lab was to investigate the Physical Layer components of my MacBook, understand how the operating system identifies network interfaces, verify the health of the Wi-Fi Network Interface Card (NIC), and practice basic Physical Layer troubleshooting.



# Learning Outcomes

After completing this lab, I can:

- Identify the Wi-Fi Network Interface Card (NIC).
- Determine the interface name used by macOS.
- Locate the MAC address of a network interface.
- Verify whether a network interface is active or inactive.
- Distinguish between a Physical Layer failure and an Internet connectivity problem.
- Enable and disable a network interface using Terminal.
- Restore network connectivity after intentionally disabling an interface.


# Environment

- Operating System: macOS
- Connection Type: Wi-Fi
- Terminal: macOS Terminal



# Lab Activities

## Part 1 — Identify Hardware Interfaces

### Command

networksetup -listallhardwareports


### Purpose

Displays all network hardware installed on the computer and maps each hardware device to its interface name.

### My Observation

Hardware Port: Wi-Fi
Device: en0
Ethernet Address: (Hidden)


### Interpretation

- My Wi-Fi adapter uses the interface name **en0**.
- The operating system successfully detected the Wi-Fi hardware.
- The interface has a valid MAC address.



## Part 2 — Inspect the Wi-Fi Interface

### Command


ifconfig en0


### Purpose

Displays detailed information about the selected network interface.

### Important Information Observed

- Interface Name: en0
- Status: Active
- IPv4 Address Assigned
- IPv6 Address Assigned
- MAC Address Present

### Interpretation

The interface is functioning normally and is connected to the wireless network.



## Part 3 — Verify Interface Status

### Command


ifconfig en0 | grep status


### Result


status: active


### Interpretation

The Wi-Fi interface is operational and communicating successfully.



## Part 4 — Simulating a Physical Layer Failure

### Disable the Interface


sudo ifconfig en0 down


### Observation

- Wi-Fi disconnected.
- Internet access stopped.
- The interface became inactive.

### Interpretation

The hardware itself was not damaged. The operating system simply stopped using the network interface.



## Part 5 — Restoring the Interface

### Command


sudo ifconfig en0 up


### Observation

- Wi-Fi reconnected successfully.
- Internet access returned.
- Interface status became active again.

### Interpretation

The Wi-Fi NIC was functioning correctly, and restoring the interface restored connectivity.


# Commands Used


networksetup -listallhardwareports

ifconfig

ifconfig en0

ifconfig en0 | grep status

sudo ifconfig en0 down

sudo ifconfig en0 up




# Key Concepts Learned

## Network Interface Card (NIC)

A Network Interface Card (NIC) is the hardware component that allows a computer to communicate on a network.

Without a functioning NIC, a device cannot send or receive network traffic.



## Interface Name

macOS identifies each network interface with a device name such as:

- en0
- en1
- bridge0
- lo0

My Wi-Fi interface is:


en0



## MAC Address

The MAC address is the unique Layer 2 identifier assigned to the network interface.

It identifies the device on the local network.



## Interface Status

### Active

The interface is operational and communicating.

### Inactive

The interface is disabled or not connected.


# Troubleshooting Exercise

## Scenario

A user reports:

> "My laptop has no Internet."

### Investigation

Check:


ifconfig en0 | grep status


### If the Result is

status: inactive

Possible causes:

- Wi-Fi disabled
- Interface disabled
- Hardware issue
- Out of wireless range

### Correct Troubleshooting Order

1. Verify interface status.
2. Enable the interface if disabled.
3. Confirm Wi-Fi is connected.
4. Test Internet connectivity.
5. Continue to higher OSI layers only if the Physical Layer is healthy.



# Engineering Insights

- A device can contain a NIC but still be unable to communicate if the operating system disables the interface.
- "Connected to Wi-Fi" and "Connected to the Internet" are different states.
- The Physical Layer must be operational before higher OSI layers can function correctly.
- Troubleshooting should begin with the simplest and lowest layer before moving upward.



# Common Misconceptions

❌ A NIC connects a computer directly to the Internet.

✔ A NIC connects a computer to a network. Internet access depends on additional devices and protocols.


❌ No Internet always means the ISP is down.

✔ The problem may simply be a disabled network interface.



# Lab Summary

This lab introduced the practical aspects of the Physical Layer by identifying the Wi-Fi NIC, inspecting interface information, verifying interface status, intentionally disabling the interface, restoring connectivity, and applying a structured troubleshooting process.