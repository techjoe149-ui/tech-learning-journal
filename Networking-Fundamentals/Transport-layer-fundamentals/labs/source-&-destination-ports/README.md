# Transport Fundamentals — Source & Destination Ports Lab

**Phase:** Transport Fundamentals
**Lesson:**  — Source & Destination Ports
**Lab:**   Observe Source & Destination Ports
**Status:** Completed

---

## 1. Objective

The purpose of this lab was to observe a real TCP connection and identify:

* Source IP address
* Source port
* Destination IP address
* Destination port
* Basic TCP connection state

The lab demonstrates how transport-layer ports identify the two endpoints involved in communication.

---

## 2. Concept

A network communication has two endpoints.

```text
CLIENT ENDPOINT                 SERVER ENDPOINT

<CLIENT-IP>:<SOURCE-PORT>  →  <SERVER-IP>:<DESTINATION-PORT>
```

The **source port** identifies the transport endpoint sending the communication.

The **destination port** identifies the transport endpoint receiving the communication.

A client commonly uses a temporary source port, while a server commonly receives requests through a known service port.

For example:

```text
<CLIENT-IP>:<TEMPORARY-PORT>  →  <SERVER-IP>:443
```

Here:

* `<CLIENT-IP>` = source IP
* `<TEMPORARY-PORT>` = source port
* `<SERVER-IP>` = destination IP
* `443` = destination port

---

## 3. Lab Environment

**Operating System:** macOS
**Tools:** Terminal, `curl`, `lsof`
**Protocol observed:** TCP

---

## 4. Procedure

A request was made to a public web server using:

```bash
curl https://example.com --limit-rate 100 & sleep 1; lsof -nP -iTCP -a -c curl
```

The command allowed the active TCP connection to be observed using `lsof`.

The raw terminal output contained machine-specific information and was therefore **not included in this documentation**.

---

## 5. Observed Connection

The connection followed this structure:

```text
<LOCAL-IP>:<SOURCE-PORT> → <REMOTE-IP>:443
```

The observed connection was in the:

```text
ESTABLISHED
```

state.

This demonstrated that:

* The local computer had a source IP and source port.
* The remote server had a destination IP and destination port.
* The client used a temporary source port.
* Port `443` was used as the destination service port.
* The TCP connection had been established.

---

## 6. Understanding the Connection

Conceptually:

```text
CLIENT                              SERVER

<LOCAL-IP>:<SOURCE-PORT> ───────→ <REMOTE-IP>:443
       Source                         Destination
```

For the response, the direction reverses:

```text
SERVER                              CLIENT

<REMOTE-IP>:443 ───────────────→ <LOCAL-IP>:<SOURCE-PORT>
   Source                            Destination
```

Therefore, a port number does not permanently mean "client port" or "server port."

Its role depends on the **direction of the communication**.

---

## 7. Key Learning

The lab demonstrated the relationship between IP addresses and ports:

```text
IP Address → identifies the host
Port       → identifies the transport endpoint/service
```

Together, they allow the two endpoints of a communication to be identified.

A simplified communication can therefore be represented as:

```text
Client IP : Client Port
        ↓
        ↓
Server IP : Server Port
```

---

## 8. Troubleshooting Insight

When examining a network connection, ask:

1. **Which host is communicating?**
2. **What is the source port?**
3. **What is the destination port?**
4. **Which direction is the communication going?**
5. **Is the TCP connection established?**

An important distinction is:

> A port's role as source or destination depends on the direction of the communication.

---

# Career & Job Relevance

## Skills Learned

* Identifying source and destination ports
* Reading basic TCP connection information
* Understanding client/server communication
* Using `lsof` to observe active network connections
* Interpreting basic network endpoint information
* Understanding the relationship between IP addresses and ports

## Relevant Job Roles

These skills commonly appear in:

* Network Technician
* Network Support Engineer
* Systems Administrator
* Network Engineer
* Cloud Support Engineer
* SOC Analyst
* Cybersecurity Analyst
* Penetration Tester

## Workplace Scenario

A user reports that they can reach a remote server but an application is not working.

A technician can inspect the connection and determine:

```text
Source IP → Source Port
Destination IP → Destination Port
Connection State
```

This helps determine whether the communication is reaching the expected service endpoint.

## How This Appears in Job Descriptions

You may encounter requirements such as:

* "Troubleshoot TCP/IP connectivity issues"
* "Analyze network connections and ports"
* "Troubleshoot network services"
* "Understand TCP/UDP protocols and port numbers"
* "Use network troubleshooting tools"
* "Monitor and analyze network traffic"

The practical ability to identify source/destination ports is part of the foundation behind these requirements.

---

# Lab Evidence & Privacy

The original terminal output contained machine-specific information, including:

* Local IP address
* Process ID
* Username
* Device information
* Remote server IP address

These details have been **excluded from the public documentation**.

The GitHub version uses placeholders such as:

```text
<LOCAL-IP>
<SOURCE-PORT>
<REMOTE-IP>
```

This preserves the technical lesson without unnecessarily exposing system-specific information.

---

# Exit Criteria

This lab is considered complete because I can:

* [x] Identify the source IP
* [x] Identify the source port
* [x] Identify the destination IP
* [x] Identify the destination port
* [x] Explain the difference between source and destination ports
* [x] Explain why the client uses a temporary source port
* [x] Explain why source/destination roles reverse in the response
* [x] Recognize `ESTABLISHED` as an active TCP connection
* [x] Use `lsof` to observe a TCP connection
* [x] Explain the client/server endpoint relationship

