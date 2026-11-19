# Transport Layer — Labs

## Overview

This directory contains hands-on labs for the **Transport Layer** of computer networking.

The labs are designed to connect Transport Layer theory with real operating-system and network behavior. The focus is not only on running commands, but on understanding what the results mean and using them to troubleshoot real connectivity problems.


## Lab Objectives

The Transport Layer labs focus on developing the ability to:

* Understand TCP and UDP communication.
* Identify source and destination ports.
* Inspect active network connections.
* Identify services listening on TCP ports.
* Understand TCP connection states.
* Test local and remote TCP connectivity.
* Observe UDP communication.
* Interpret connection success, refusal, and timeout.
* Distinguish Layer 3 connectivity from Layer 4 connectivity.
* Troubleshoot common Transport Layer failures.
* Recognize common Transport Layer security threats.
* Apply a structured enterprise troubleshooting methodology.



### `transport-layer-lab.md`

The main hands-on lab covering:

* TCP connection inspection
* UDP connection inspection
* Listening services
* Ports and sockets
* Localhost and loopback
* TCP connectivity testing
* TCP timeout behavior
* UDP communication
* DNS connectivity testing
* Layer 4 troubleshooting
* Enterprise troubleshooting scenarios
* Transport Layer security threats
* Practical troubleshooting methodology



## Tools Used

The labs use native networking tools available on macOS, including:

| Tool           | Purpose                                             
| -------------- | ------------------|---------------------------------------|
| `lsof`         | Inspect processes, sockets, ports, and active connections |
| `nc`           | Test TCP/UDP connectivity to specific ports               |
| `ping`         | Verify IP-level reachability                              |
| `networksetup` | Inspect network configuration                             |


## Key Skills Demonstrated

By completing this lab, I can demonstrate practical ability to:

**Inspect**

* Active TCP connections
* UDP communication
* Listening services
* Source and destination ports
* TCP connection states

**Test**

* Local TCP services
* Remote TCP services
* Specific destination ports
* DNS connectivity
* TCP timeout behavior

**Troubleshoot**

* Connection failures
* Connection refusals
* Connection timeouts
* Service availability
* Port accessibility
* Firewall and ACL possibilities
* Layer 3 vs Layer 4 failures

**Secure**

* Identify exposed services
* Understand port scanning
* Recognize SYN floods
* Recognize UDP floods
* Understand TCP reset attacks
* Reduce unnecessary attack surface



## Troubleshooting Philosophy

The labs follow a structured troubleshooting approach rather than random configuration changes.

When an application fails, the investigation progresses systematically:

```text
Physical Connectivity
        ↓
Layer 2 Connectivity
        ↓
IP Configuration
        ↓
Gateway / Routing
        ↓
Destination Reachability
        ↓
Protocol + Port
        ↓
Transport Connectivity
        ↓
Application
```

The objective is to determine:

> **What is failing, at which layer, and what evidence proves it?**


## Completed Lab

Transport Layer — Hands-On Troubleshooting Lab | ✅ Completed |


## Evidence

The completed lab contains real command output captured from a macOS system, including:

* Active TCP/UDP connections
* Listening TCP services
* Successful local TCP connection
* Successful remote HTTPS connection
* TCP timeout
* UDP traffic
* Successful TCP connection to DNS port 53

This provides practical evidence that the concepts were tested against a real operating system rather than studied only theoretically.

