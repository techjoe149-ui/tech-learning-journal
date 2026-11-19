# Transport Fundamentals — UDP Lab

**Phase:** Transport Fundamentals
**Lesson:** 5 — UDP Lab
**Status:** Completed

---

## 1. Objective

The purpose of this lab was to observe real UDP traffic and identify:

* Source IP address
* Source port
* Destination IP address
* Destination port
* Transport protocol
* The direction of a UDP request and response

The lab also demonstrated the connectionless nature of UDP.

---

## 2. Concept

UDP is a **connectionless transport protocol**.

Unlike TCP, UDP does not first establish a TCP-style connection before sending data.

A simplified UDP communication looks like:

```text
CLIENT                              SERVER

<CLIENT-IP>:<SOURCE-PORT>  ─────→  <SERVER-IP>:53
```

The server can then send a response:

```text
SERVER                              CLIENT

<SERVER-IP>:53  ───────────────→  <CLIENT-IP>:<SOURCE-PORT>
```

The source and destination roles reverse because the direction of communication has changed.

---

## 3. Lab Environment

**Operating System:** macOS
**Tools:** Terminal, `nslookup`, `tcpdump`
**Protocol observed:** UDP
**Application/service observed:** DNS

---

## 4. Procedure

A DNS lookup was first generated using:

```bash
nslookup example.com
```

This produced a DNS response and confirmed that DNS communication was occurring.

UDP traffic associated with DNS was then captured using:

```bash
sudo tcpdump -ni en0 udp port 53
```

A DNS lookup was performed while the capture was running.

The raw terminal output contained machine-specific information and was therefore **not included in this public documentation**.

---

## 5. Observed UDP Request

The capture showed a UDP DNS request following this structure:

```text
<LOCAL-IP>:<SOURCE-PORT> → <DNS-SERVER-IP>:53
```

For the observed request:

```text
<LOCAL-IP>:56004 → <DNS-SERVER-IP>:53
```

The fields were interpreted as:

* `<LOCAL-IP>` → source IP
* `56004` → source port
* `<DNS-SERVER-IP>` → destination IP
* `53` → destination port
* UDP → transport protocol

Port `53` is the standard port associated with DNS.

---

## 6. Observed UDP Response

The capture also showed the DNS server responding:

```text
<DNS-SERVER-IP>:53 → <LOCAL-IP>:56004
```

The roles therefore reversed:

```text
REQUEST

Client                              DNS Server
<CLIENT-IP>:56004  ─────────────→  <SERVER-IP>:53
     Source                         Destination


RESPONSE

Client                              DNS Server
<CLIENT-IP>:56004  ←─────────────  <SERVER-IP>:53
  Destination                          Source
```

The same two port numbers are used, but their **source/destination roles depend on the direction of the communication**.

---

## 7. Understanding Connectionless Communication

The UDP capture did not show a TCP-style connection establishment.

The basic communication was:

```text
Client → UDP datagram → Server
Client ← UDP response  ← Server
```

UDP itself does not provide:

* Connection establishment
* Guaranteed delivery
* Automatic retransmission
* Guaranteed ordering

This makes UDP a simpler transport protocol than TCP.

---

## 8. Important Observation

The lab demonstrated that:

> **A port number does not permanently belong to either the client or server.**

For example:

```text
Client → Server

Client:56004 → Server:53
```

Here:

* `56004` = source port
* `53` = destination port

For the response:

```text
Server → Client

Server:53 → Client:56004
```

Here:

* `53` = source port
* `56004` = destination port

The role changes because the **direction changes**.

---

## 9. Troubleshooting Insight

When examining UDP traffic, identify:

1. Source IP
2. Source port
3. Destination IP
4. Destination port
5. Transport protocol
6. Direction of communication

A useful troubleshooting model is:

```text
Which host?
     ↓
Which port?
     ↓
Which transport protocol?
     ↓
Which direction?
```

This helps distinguish basic addressing and transport information when investigating network communication.

---

# Career & Job Relevance

## Skills Learned

* Understanding UDP communication
* Identifying UDP source and destination ports
* Reading basic packet-capture output
* Using `tcpdump`
* Understanding DNS at a basic transport level
* Understanding connectionless communication
* Interpreting request and response directions

## Relevant Job Titles

These skills are commonly used in roles such as:

* Network Technician
* Network Support Engineer
* Systems Administrator
* Network Engineer
* Cloud Support Engineer
* SOC Analyst
* Cybersecurity Analyst
* Penetration Tester

## Workplace Scenario

A technician receives a report that DNS resolution is not working.

They can capture traffic and determine whether the computer is actually sending DNS requests:

```text
<Client-IP>:<Source-Port> → <DNS-Server-IP>:53
```

They can then check whether a response is returning:

```text
<DNS-Server-IP>:53 → <Client-IP>:<Source-Port>
```

This provides basic evidence about whether DNS traffic is being generated and whether responses are returning.

## How This Appears in Job Descriptions

You may encounter requirements such as:

* "Troubleshoot TCP/IP and UDP connectivity"
* "Analyze network traffic using packet capture tools"
* "Troubleshoot DNS and network services"
* "Understand TCP/UDP protocols"
* "Use tools such as tcpdump or Wireshark"
* "Analyze network communications and ports"

The ability to read basic UDP traffic is part of the foundation behind these requirements.

---

# Lab Evidence & Privacy

The original capture contained machine-specific information, including:

* Local IP address
* Local source ports
* Remote IP addresses
* Device/interface information
* DNS query information

These details have been **sanitized or replaced with placeholders** in this public version.

Example:

```text
<LOCAL-IP>:<SOURCE-PORT> → <DNS-SERVER-IP>:53
```

This preserves the technical evidence without unnecessarily exposing system-specific information.

---

# Exit Criteria

This lab is considered complete because I can:

* [x] Identify UDP traffic
* [x] Identify a source IP
* [x] Identify a source port
* [x] Identify a destination IP
* [x] Identify a destination port
* [x] Explain UDP as connectionless
* [x] Explain that UDP does not guarantee delivery
* [x] Explain that UDP does not provide automatic retransmission
* [x] Identify DNS port 53
* [x] Explain request and response direction
* [x] Explain why source and destination roles reverse
* [x] Use `tcpdump` to observe UDP traffic
