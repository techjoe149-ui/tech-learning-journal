# Lab 9 — Routing Fundamentals Integration Lab

## 1. Overview

This lab is the final integration and assessment lab for the Routing Fundamentals section.

Unlike the previous labs, this lab introduces no new routing concepts. Instead, it combines the practical skills developed throughout Labs 1–8 into one realistic network troubleshooting scenario.

The objective was to determine why a workstation could communicate with its local gateway but could not reach a remote server.

The investigation followed an evidence-based troubleshooting process:

```text
IPv4 Configuration
        ↓
Network Identification
        ↓
Gateway Identification
        ↓
Route Selection
        ↓
Gateway Reachability
        ↓
Destination Reachability
        ↓
Path Analysis
        ↓
Failure Localization
```

---

# 2. Scenario — Problem Being Solved

A workstation user reports:

> "I'm connected to Wi-Fi, but I can't reach the company server."

The workstation must communicate with a remote server located on another IP network.

The task is to determine:

* Whether the local interface is functioning.
* What IPv4 network the workstation belongs to.
* What default gateway is being used.
* Which route is selected for the remote destination.
* Whether the gateway is reachable.
* Whether the remote destination is reachable.
* How far traffic travels toward the destination.
* Where troubleshooting should be focused based on the available evidence.

---

# 3. Architecture

```text
                    Local Network
                  192.168.xxx.0/24
                         │
                         │
                 ┌───────┴───────┐
                 │      Mac      │
                 │ 192.168.xxx.x │
                 │      en0      │
                 └───────┬───────┘
                         │
                         │
                         ▼
                 Default Gateway
                  192.168.xxx.1
                         │
                         │
                  Other Networks
                         │
                         ▼
                  Remote Network
                   10.20.30.0/24
                         │
                         ▼
                 Remote Server
                   10.20.30.50
```

Environment-specific addresses are masked in this documentation where appropriate.

---

# 4. Objectives

* Identify the workstation's IPv4 configuration.
* Identify the local network.
* Identify the default gateway.
* Inspect the routing table.
* Determine the route selected for a remote destination.
* Apply route-matching and longest-prefix reasoning.
* Identify the next hop and outgoing interface.
* Test gateway reachability.
* Test remote destination reachability.
* Use traceroute to obtain path evidence.
* Distinguish local connectivity failure from remote-path failure.
* Localize the failure using evidence.
* Apply structured troubleshooting reasoning.
* Connect foundational routing knowledge to real IT/networking work.

---

# 5. Environment

| Item               | Details                                              |
| ------------------ | ---------------------------------------------------- |
| Operating System   | macOS                                                |
| Network Interface  | `en0` — Wi-Fi                                        |
| IPv4 Address       | `192.168.xxx.xxx`                                    |
| Subnet Mask        | `255.255.255.0` (`/24`)                              |
| Local Network      | `192.168.xxx.0/24`                                   |
| Default Gateway    | `192.168.xxx.1`                                      |
| Remote Destination | `10.20.30.50`                                        |
| Tools              | `ifconfig`, `route`, `netstat`, `ping`, `traceroute` |

Environment-specific information has been masked for public documentation.

---

# 6. Important Concepts

## 6.1 IPv4 Address

An IPv4 address identifies a network interface on an IP network.

The workstation had an IPv4 address in the form:

```text
192.168.xxx.xxx
```

This address was assigned to the Mac's `en0` Wi-Fi interface.

---

## 6.2 Subnet Mask

The subnet mask determines which portion of the IPv4 address represents the network and which portion represents the host.

The mask used was:

```text
255.255.255.0
```

which is equivalent to:

```text
/24
```

---

## 6.3 Network Address

With a `/24` mask, the first three octets identify the network.

Therefore:

```text
192.168.xxx.xxx
255.255.255.0
```

produces the local network:

```text
192.168.xxx.0/24
```

---

## 6.4 Default Gateway

The default gateway is the router used when the destination does not match a more-specific route in the routing table.

The gateway identified during the lab was:

```text
192.168.xxx.1
```

---

## 6.5 Route Selection

A host compares a destination against its routing table.

If a destination matches a more-specific route, that route is preferred over the default route.

If no more-specific route matches, the default route is used.

---

## 6.6 Next Hop

The next hop is the device to which the packet is forwarded next.

For the remote server in this lab, the next hop from the workstation was the default gateway:

```text
192.168.xxx.1
```

---

# 7. Step 1 — Inspect the Network Interface

The network interfaces were inspected using:

```bash
ifconfig
```

The Wi-Fi interface was:

```text
en0
```

The interface reported:

```text
UP
RUNNING
```

This provided evidence that the interface was enabled and had an active connection.

The IPv4 configuration was then isolated using:

```bash
ifconfig en0 | grep "inet "
```

The workstation returned an IPv4 address in the:

```text
192.168.xxx.xxx
```

range with a `/24` subnet mask.

---

# 8. Step 2 — Identify the Local Network

The IPv4 address and subnet mask were used to determine the local network.

```text
Host:
192.168.xxx.xxx

Mask:
255.255.255.0

Network:
192.168.xxx.0/24
```

This established the local network boundary.

---

# 9. Step 3 — Identify the Default Gateway

The default route was inspected using:

```bash
route -n get default
```

The result identified:

```text
Destination: default
Gateway:     192.168.xxx.1
Interface:   en0
```

Therefore:

```text
Default Gateway = 192.168.xxx.1
```

---

# 10. Step 4 — Inspect the Routing Table

The routing table was inspected using:

```bash
netstat -rn -f inet
```

Important entries included:

```text
default        192.168.xxx.1        en0
192.168.xxx    link#4               en0
```

This demonstrated that the workstation had:

1. A directly connected local-network route.
2. A default route through the gateway.

---

# 11. Step 5 — Determine the Route to the Remote Destination

The remote server was:

```text
10.20.30.50
```

The selected route was determined using:

```bash
route -n get 10.20.30.50
```

The system returned a result equivalent to:

```text
destination: default
gateway:     192.168.xxx.1
interface:   en0
```

Therefore:

```text
10.20.30.50
      ↓
Default Route
      ↓
192.168.xxx.1
      ↓
en0
```

---

# 12. Route Selection Reasoning

The remote destination:

```text
10.20.30.50
```

does not belong to:

```text
192.168.xxx.0/24
```

Therefore, the directly connected local route does not match the destination.

The default route is consequently selected.

This is an example of route matching and longest-prefix reasoning.

---

# 13. Step 6 — Test Gateway Reachability

The gateway was tested using:

```bash
ping -c 4 192.168.xxx.1
```

The result showed:

```text
4 packets transmitted
4 packets received
0.0% packet loss
```

Therefore:

```text
Mac → Gateway
     ✅
```

The local gateway was reachable.

---

# 14. What Gateway Reachability Proves

Successful gateway communication provides evidence that:

* The network interface is functioning.
* The workstation has local network connectivity.
* The gateway is reachable.
* Local communication is working.

It does **not** prove that the remote server is reachable.

---

# 15. Step 7 — Test Remote Destination Reachability

The remote server was tested using:

```bash
ping -c 4 10.20.30.50
```

The workstation received:

```text
Request timeout
```

for the ICMP requests.

Therefore:

```text
Mac → Gateway       ✅
Mac → Remote Server ❌
```

This established that local gateway communication was working while communication with the remote destination was not confirmed.

---

# 16. Step 8 — Analyze the Path

Traceroute was used:

```bash
traceroute 10.20.30.50
```

The path showed:

```text
Hop 1   Local gateway          ✅
Hop 2                          *
Hop 3   Intermediate router    ✅
Hop 4+                         *
...
Destination                    ❌
```

The actual environment-specific addresses have been masked.

---

# 17. Interpretation of Traceroute

The first hop corresponded to the local gateway.

An intermediate router further along the path also responded.

This provided evidence that traffic progressed beyond the local network.

However, the `* * *` responses did not automatically indicate that those routers were broken.

A router may forward traffic while not responding to traceroute probes.

---

# 18. Important Distinction — Hop Response vs Destination Response

A responding intermediate hop does not prove that the final destination is reachable.

Traffic can successfully pass through several routers while the final destination:

* Is offline.
* Is unavailable.
* Blocks ICMP.
* Has a firewall or ACL.
* Has a routing problem.
* Has a return-path problem.

Therefore, traceroute is used as **path evidence**, not as automatic proof of the exact root cause.

---

# 19. Failure Localization

The evidence collected was:

```text
Interface active                  ✅
IPv4 configuration                ✅
Local network identified          ✅
Default route exists              ✅
Gateway reachable                 ✅
Remote destination reachable      ❌
Intermediate path evidence        ✅
```

This allows the investigation to move away from the local workstation and gateway.

The strongest conclusion was:

```text
The failure is likely somewhere beyond the local network/gateway.
```

---

# 20. Troubleshooting Decision

Possible causes included:

```text
A. Remote server unavailable
B. Firewall/ACL filtering
C. Routing problem beyond the gateway
D. Return-path problem
E. Another remote-side network failure
```

The available evidence was insufficient to identify one exact cause.

Therefore, the strongest evidence-based conclusion was:

```text
Multiple remote-side causes remain possible.
```

---

# 21. Evidence-Based Troubleshooting

The investigation followed this sequence:

```text
Identify host
     ↓
Identify network
     ↓
Identify gateway
     ↓
Inspect routing table
     ↓
Determine selected route
     ↓
Test gateway
     ↓
Test destination
     ↓
Trace path
     ↓
Compare evidence
     ↓
Localize failure
```

This prevents assumptions from replacing evidence.

---

# 22. Troubleshooting Commands

### Inspect interface

```bash
ifconfig
```

### Inspect IPv4 configuration

```bash
ifconfig en0 | grep "inet "
```

### Inspect default route

```bash
route -n get default
```

### Inspect routing table

```bash
netstat -rn -f inet
```

### Determine route to destination

```bash
route -n get 10.20.30.50
```

### Test gateway

```bash
ping -c 4 192.168.xxx.1
```

### Test destination

```bash
ping -c 4 10.20.30.50
```

### Trace destination path

```bash
traceroute 10.20.30.50
```

---

# 23. What Each Tool Tells Us

| Tool           | Purpose                          |
| -------------- | -------------------------------- |
| `ifconfig`     | Interface and IP configuration   |
| `route -n get` | Selected route for a destination |
| `netstat -rn`  | Routing table                    |
| `ping`         | Reachability testing             |
| `traceroute`   | Path/hop investigation           |

No individual tool provided the complete diagnosis.

The diagnosis came from **combining the evidence** produced by the tools.

---

# 24. Important Troubleshooting Lesson

Network troubleshooting should move from known facts toward unknown areas.

In this lab:

```text
Local Interface
      ↓
Local Network
      ↓
Gateway
      ↓
Remote Path
      ↓
Destination
```

Once the gateway was proven reachable, repeatedly investigating the local Wi-Fi connection would not have been the most evidence-based next step.

The evidence indicated that investigation should move beyond the local network.

---

# 25. Root-Cause Reasoning

The exact root cause could not be established from the available evidence.

What could be established was the **failure boundary**:

```text
Local workstation → gateway       WORKING
Beyond gateway → destination      NOT CONFIRMED
```

Possible remote-side causes remained under investigation.

This demonstrates an important professional distinction:

> **Failure localization is not the same as root-cause identification.**

---

# 26. Resolution

Because the available evidence did not identify a single root cause, the correct resolution at this stage was **not to claim that a particular device or service was responsible**.

The appropriate next action would be to continue investigating the remote network using additional evidence from the systems beyond the local gateway.

The important result of this lab was the successful localization of the problem to the remote path rather than incorrectly blaming the workstation.

---

# 27. Security Considerations

Routing information can expose details about network infrastructure.

Information such as:

* Internal IP addresses
* Gateway addresses
* Routing tables
* Network topology
* Traceroute results

should be handled carefully when documenting or publishing troubleshooting results.

Environment-specific information should therefore be masked in public-facing documentation.

---

# 28. Lessons Learned

* An IPv4 address identifies a host interface on an IP network.
* A subnet mask determines the network boundary.
* A `/24` network keeps the first three octets fixed.
* A destination outside the local network requires routing.
* The default gateway handles destinations without a more-specific matching route.
* `route -n get` reveals the route selected for a destination.
* A reachable gateway does not guarantee remote connectivity.
* Traceroute provides path evidence.
* Missing traceroute responses do not automatically indicate broken routers.
* Intermediate-hop responses do not prove final-destination reachability.
* Troubleshooting should be evidence-based.
* Failure localization and root-cause identification are different tasks.

---

# 29. Practical Skills Demonstrated

The following practical skills were demonstrated:

### Networking Skills

* IPv4 addressing
* Subnet-mask interpretation
* Network-address identification
* Default-gateway identification
* Routing-table inspection
* Route matching
* Longest-prefix reasoning
* Next-hop identification
* Outgoing-interface identification
* Reachability testing
* Path analysis
* Failure localization

### Troubleshooting Skills

* Establishing a baseline
* Testing from local to remote
* Separating local failure from remote failure
* Gathering multiple forms of evidence
* Avoiding premature root-cause assumptions
* Building an evidence chain
* Identifying the next troubleshooting domain

### Command-Line Skills

* `ifconfig`
* `netstat`
* `route`
* `ping`
* `traceroute`

---

# 30. Career & Job Relevance

The skills demonstrated in this lab are not merely academic networking exercises. They represent foundational tasks performed in several real IT and networking roles.

## 30.1 Job Titles That Use These Skills

| Job Title                                | Relevance of These Skills |
| ---------------------------------------- | ------------------------- |
| IT Support Technician                    | High                      |
| IT Support Specialist                    | High                      |
| Network Support Technician               | Very High                 |
| NOC Technician / NOC Analyst             | Very High                 |
| Network Administrator                    | Very High                 |
| Systems Administrator                    | High                      |
| Network Engineer                         | Foundational              |
| Cloud Support Engineer                   | Foundational              |
| Cybersecurity Analyst                    | Foundational              |
| Security Operations Center (SOC) Analyst | Foundational              |

The important distinction is that this lab does **not** make someone a Network Engineer or Cybersecurity Analyst by itself.

Instead, it gives you a foundation that those roles build upon.

---

# 31. Workplace Scenario — NOC Technician

A monitoring system reports:

> "Server unreachable."

A NOC technician might:

```text
Check local/interface status
        ↓
Check IP configuration
        ↓
Check gateway
        ↓
Check routing
        ↓
Test destination
        ↓
Trace path
        ↓
Determine failure domain
        ↓
Escalate if necessary
```

This is substantially the same reasoning practiced in this lab.

The technician may then escalate the issue to the network or systems team with evidence rather than simply saying:

> "The server is down."

---

# 32. Workplace Scenario — Network Administrator

A user reports that an internal application cannot be reached.

The administrator may investigate:

* The user's IP configuration.
* Subnet membership.
* Default gateway.
* Routing table.
* Network path.
* Reachability of the application server.
* Possible routing or filtering problems.

The administrator needs to understand whether the problem originates from:

```text
Endpoint
   ↓
LAN
   ↓
Gateway
   ↓
Routing
   ↓
Firewall
   ↓
Remote Network
   ↓
Server
```

---

# 33. Workplace Scenario — IT Support Specialist

An employee says:

> "The internet is connected, but this particular service doesn't work."

Instead of immediately restarting the computer, an IT support specialist can determine:

1. Does the interface have an IP?
2. What network is the device on?
3. Is the gateway reachable?
4. Is the destination reachable?
5. Does the routing table contain an appropriate route?
6. Where does the path stop responding?

This turns troubleshooting into a structured process.

---

# 34. Workplace Scenario — Cybersecurity

A security analyst investigating suspicious network behavior may need to understand:

```text
Where is this host sending traffic?
        ↓
Which gateway is being used?
        ↓
Which network is the destination on?
        ↓
What path does the traffic take?
        ↓
Is the route expected?
```

Routing fundamentals therefore form part of the foundation for network security analysis.

---

# 35. How These Skills Appear in Real Job Requirements


### Requirement Example 1

> **"Troubleshoot TCP/IP connectivity issues."**

What this means:

You should understand how IP communication works and be able to systematically determine where connectivity is failing.

---

### Requirement Example 2

> **"Working knowledge of IPv4, subnetting, routing, DNS and DHCP."**

This indicates that the employer expects foundational network knowledge.

The IPv4, subnetting and routing portions directly connect to the skills practiced here.

---

### Requirement Example 3

> **"Use network troubleshooting tools such as ping, traceroute and routing-table utilities."**

This is a direct match with the practical command-line work performed in this lab.

---

### Requirement Example 4

> **"Diagnose network connectivity problems and escalate complex issues to the network engineering team."**

The important skill here is not necessarily fixing everything yourself.

It is being able to:

```text
Investigate
    ↓
Collect evidence
    ↓
Localize the problem
    ↓
Document findings
    ↓
Escalate intelligently
```

That is exactly the troubleshooting mindset practiced here.

---

# 36. How to Recognize Your Skills in Job Descriptions

When you see these phrases in a job advertisement, recognize the connection:

| Job requirement language     | Skill you have started developing               |
| ---------------------------- | ----------------------------------------------- |
| TCP/IP troubleshooting       | Network connectivity troubleshooting            |
| IPv4 networking              | IPv4 addressing                                 |
| Subnetting                   | Network/subnet identification                   |
| Routing fundamentals         | Routing-table and route-selection work          |
| Default gateways             | Gateway identification                          |
| Network diagnostics          | `ping`, `traceroute`, route inspection          |
| Troubleshooting connectivity | Evidence-based failure localization             |
| Network monitoring           | Understanding normal network paths              |
| NOC support                  | Structured network troubleshooting              |
| Network administration       | Foundational routing and connectivity knowledge |

This is important because job advertisements often describe skills using **industry terminology rather than the exact terminology used in learning materials**.

---

# 37. What You Can Honestly Claim at This Stage

After completing this section, an accurate portfolio/CV statement would be:

> **Hands-on foundational experience with IPv4 addressing, subnet identification, routing-table analysis, route selection, gateway troubleshooting, reachability testing and network path analysis using command-line networking tools.**

A stronger practical statement would be:

> **Performed structured network troubleshooting by analyzing IPv4 configuration, routing tables, default gateways, route selection, gateway reachability and traceroute results to localize connectivity failures.**

These statements describe what was actually practiced without exaggerating the level of expertise.

---

# 38. Foundation-to-Advanced Connection

The concepts demonstrated here form the foundation for more advanced networking work.

```text
IPv4 Addressing
      ↓
Subnetting
      ↓
Routing Tables
      ↓
Route Selection
      ↓
Next-Hop Forwarding
      ↓
Path Analysis
      ↓
Troubleshooting
      ↓
Advanced Routing
      ↓
Cloud Networking
      ↓
Network Security
```

Future technologies will build on these same fundamentals.

---

# 39. Connection to Cybersecurity

Routing knowledge is directly relevant to cybersecurity.

A security professional may need to determine:

* Where traffic is being sent.
* Whether traffic is leaving the expected network.
* Whether a gateway has changed.
* Whether a route has unexpectedly changed.
* Whether traffic is being filtered.
* Where network segmentation occurs.
* Whether a host can reach a protected network.

Understanding normal routing behavior makes abnormal routing behavior easier to recognize.

---

# 40. Final Practical Workflow

A foundational routing troubleshooting workflow established through the Routing Fundamentals labs is:

```text
1. Check interface
        ↓
2. Identify IPv4 address
        ↓
3. Identify local network
        ↓
4. Identify gateway
        ↓
5. Inspect routing table
        ↓
6. Determine route to destination
        ↓
7. Identify next hop/interface
        ↓
8. Test gateway
        ↓
9. Test destination
        ↓
10. Trace the path
        ↓
11. Compare evidence
        ↓
12. Localize the failure
        ↓
13. Investigate the likely failure domain
        ↓
14. Document/escalate findings
```

---

# 41. Lab Evidence Summary

| Investigation              | Result                            |
| -------------------------- | --------------------------------- |
| Wi-Fi interface            | Active                            |
| IPv4 configuration         | Valid                             |
| Local network              | Identified                        |
| Default gateway            | Identified                        |
| Routing table              | Inspected                         |
| Route to remote server     | Default route selected            |
| Gateway reachability       | Successful                        |
| Remote server reachability | Failed                            |
| Path analysis              | Traffic progressed beyond gateway |
| Failure localization       | Beyond local network              |
| Exact root cause           | Not conclusively established      |

---

# 42. Conclusion

Lab 9 successfully integrated the Routing Fundamentals skills developed throughout Labs 1–8.

The investigation demonstrated that a workstation can have:

* A functioning network interface.
* A valid IPv4 configuration.
* A valid routing table.
* A reachable default gateway.

while still being unable to reach a remote destination.

The correct response is not to immediately assume that the workstation or gateway is broken.

Instead, evidence must be collected progressively to determine where the failure occurs.

The final troubleshooting conclusion was:

> **The local workstation and gateway were functioning, while the failure was likely somewhere beyond the local network; additional investigation would be required to establish the exact remote-side cause.**

The lab also demonstrated how foundational networking knowledge translates directly into practical IT, NOC, network administration, systems administration, cloud and cybersecurity work.

---

# 43. Result

## LAB 9 — COMPLETE ✅

## ROUTING FUNDAMENTALS — COMPLETE ✅

The skills developed in this section now form the networking foundation upon which the next stages of the technical roadmap can build.
