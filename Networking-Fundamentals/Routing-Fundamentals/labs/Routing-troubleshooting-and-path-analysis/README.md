# Lab 4 — Routing Troubleshooting & Path Analysis

## 1. Overview

This lab focused on using multiple host-side networking tools to troubleshoot a failed connection to a remote IPv4 destination.

Unlike earlier routing labs that focused primarily on understanding route selection, this lab introduced a structured troubleshooting workflow:

```text
Problem
   ↓
Collect evidence
   ↓
Check local configuration
   ↓
Check route selection
   ↓
Check next-hop connectivity
   ↓
Trace the path
   ↓
Eliminate confirmed-good components
   ↓
Narrow the fault domain
```

The lab was performed on a real macOS system using an active network connection.

All network-identifying information in this document has been masked.



# 2. Scenario — Problem Being Solved

A host was unable to reach a remote destination:

```text
10.x.x.x
```

The host had network connectivity and could reach its default gateway, but traffic to the remote destination failed.

The objective was therefore not simply to ask:

> "Why doesn't ping work?"

Instead, the investigation asked:

> "At what point in the network path does communication appear to fail?"

-

# 3. Architecture

The practical environment consisted of:

```text
Mac Host
   |
   | en0
   |
Local Network
   |
   ▼
Default Gateway
   |
   ▼
Upstream Router
   |
   ▼
Additional Routers
   |
   ▼
Remote Network
   |
   ▼
Remote Destination
```

### Components involved

* macOS host
* `en0` network interface
* IPv4 addressing
* Local subnet
* Default gateway
* ARP
* Routing table
* Multiple upstream routers
* Remote IPv4 destination
* ICMP
* Traceroute



# 4. Objectives

By completing this lab, I aimed to learn how to:

* Troubleshoot an unreachable remote destination.
* Verify the host's IPv4 configuration.
* Verify the default route.
* Verify the default gateway.
* Verify gateway MAC resolution.
* Determine the route selected for a destination.
* Test gateway connectivity.
* Test destination connectivity.
* Trace the path toward a remote destination.
* Interpret traceroute hops.
* Understand the meaning of `* * *`.
* Distinguish local problems from upstream problems.
* Narrow a fault domain using evidence.
* Avoid making unsupported conclusions from a single failed ping.



# 5. Environment

| Item                  | Details               |
| --------------------- | --------------------- |
| Device                | Mac                   |
| Operating System      | macOS                 |
| Interface             | `en0`                 |
| Connection            | Wi-Fi                 |
| Protocol              | IPv4                  |
| Primary routing tool  | `netstat -rn -f inet` |
| Route inspection      | `route -n get`        |
| Connectivity testing  | `ping`                |
| Path analysis         | `traceroute`          |
| Layer 2 investigation | `arp`                 |

Real IP addresses, MAC addresses and network details have been intentionally masked.



# 6. Commands Used

## 6.1 `ipconfig getifaddr en0`

```bash
ipconfig getifaddr en0
```

### Use

Displays the IPv4 address currently assigned to the `en0` interface.

This verifies that the host has an IPv4 address.



## 6.2 `route -n get default`

```bash
route -n get default
```

### Use

Displays the route information for the default route.

It identifies:

* Default gateway
* Interface
* Routing status



## 6.3 `netstat -rn -f inet`

```bash
netstat -rn -f inet
```

### Use

Displays the IPv4 routing table.

It allows us to determine:

* Connected networks
* Default route
* Specific routes
* Gateways
* Interfaces



## 6.4 `route -n get <destination>`

Example:

```bash
route -n get <REMOTE_DESTINATION>
```

### Use

Shows the specific route macOS would select for a particular destination.

This is useful for determining:

* Selected route
* Next hop
* Interface
* Whether the default route is being used



## 6.5 `arp -a`

```bash
arp -a
```

### Use

Displays the host's ARP cache.

It helps determine whether an IPv4 address has a known Layer 2 MAC-address mapping.



## 6.6 `ping`

Example:

```bash
ping -c 4 <DESTINATION>
```

### Use

Tests whether a destination responds to ICMP Echo Requests.

Ping provides evidence about reachability, but failure does not automatically prove that the destination is nonexistent.



## 6.7 `traceroute`

Example:

```bash
traceroute <DESTINATION>
```

### Use

Attempts to reveal the routers/hops encountered while traffic travels toward a destination.

This helps identify how far along the path communication appears to progress.



## 6.8 TCP traceroute

```bash
traceroute -P tcp <DESTINATION>
```

### Use

Performs traceroute using TCP probes rather than the default traceroute probe type.

This provides another perspective when different traffic types may be treated differently by routers or firewalls.



# 7. Baseline Investigation

The host was first inspected to establish its normal network state.

The host had:

```text
IPv4 address: <MASKED_HOST_IP>
Interface: en0
Default gateway: <MASKED_GATEWAY_IP>
```

The routing table contained a default route:

```text
default → <MASKED_GATEWAY_IP> → en0
```

This established that the host had a route for destinations that did not have a more-specific route.



# 8. Test 1 — Verify the Default Gateway

The gateway was identified using:

```bash
route -n get default
```

The result showed:

```text
gateway: <MASKED_GATEWAY_IP>
interface: en0
```

The gateway was then tested using:

```bash
ping -c 4 <MASKED_GATEWAY_IP>
```

The gateway responded successfully.

### Result

```text
4 packets transmitted
4 packets received
0.0% packet loss
```

### Interpretation

The host could successfully communicate with its immediate gateway.

This provided evidence against:

* Interface failure
* Local link failure
* Immediate gateway failure



# 9. Test 2 — Verify Gateway MAC Resolution

The ARP cache was inspected:

```bash
arp -a | grep <MASKED_GATEWAY_IP>
```

The gateway had a MAC address associated with it.

Example:

```text
<MASKED_GATEWAY_IP>
    ↓
<MASKED_GATEWAY_MAC>
```

### Interpretation

The host had a Layer 2 mapping for the gateway.

This demonstrated the relationship:

```text
Gateway IPv4
     ↓
ARP
     ↓
Gateway MAC
```

This also reinforced an important concept:

> Routing identifies the next hop; ARP identifies the MAC address needed for local Layer 2 delivery.



# 10. Test 3 — Determine the Route to the Remote Destination

The remote destination was:

```text
<MASKED_REMOTE_IP>
```

The following command was used:

```bash
route -n get <MASKED_REMOTE_IP>
```

The result showed:

```text
destination: default
gateway: <MASKED_GATEWAY_IP>
interface: en0
```

### Interpretation

The host did not have a more-specific route for the destination.

Therefore:

```text
Remote Destination
       ↓
No specific route
       ↓
Default Route
       ↓
Default Gateway
       ↓
en0
```

The host's routing decision was therefore functioning as expected.


# 11. Test 4 — Ping the Remote Destination

The remote destination was tested:

```bash
ping -c 4 <MASKED_REMOTE_IP>
```

The result was:

```text
Request timeout
```

with:

```text
100% packet loss
```

### Initial observation

The destination did not respond to ICMP Echo Requests.

However, this did **not** prove that the destination IP did not exist.

Possible explanations included:

* Destination host unavailable
* Destination network unreachable
* Firewall filtering
* ICMP blocked
* Routing problem beyond the local network
* Failure somewhere along the upstream path

Therefore, additional evidence was required.


# 12. Test 5 — Trace the Network Path

The command:

```bash
traceroute <MASKED_REMOTE_IP>
```

was used.

The traceroute showed multiple responding hops.

The actual addresses have been masked, but the path conceptually looked like:

```text
Hop 1   Default Gateway
          ↓
Hop 2   Upstream Router
          ↓
Hop 3   Another Router
          ↓
Hop 4   Another Router
          ↓
Hop 5   Another Router
          ↓
Hop 6   Upstream Router
          ↓
Hop 7+  No responses
          ↓
Remote Destination
```

The important observation was that the traffic reached multiple routers beyond the local gateway.



# 13. Understanding `* * *`

Later traceroute hops showed:

```text
* * *
```

This was initially interpreted as:

> "The network is down."

That interpretation was corrected.

### Correct interpretation

`* * *` means:

> The traceroute probe did not receive a response from that hop.

It does **not automatically mean**:

* The router is down.
* The network is down.
* The destination does not exist.

A router may intentionally:

* Ignore traceroute probes
* Rate-limit responses
* Filter traffic
* Suppress diagnostic responses

Therefore:

```text
* * *
```

must be treated as **evidence of no response**, not definitive proof of failure.



# 14. Test 6 — TCP Traceroute

The following command was tested:

```bash
traceroute -P tcp <MASKED_REMOTE_IP>
```

### Result

The TCP traceroute returned:

```text
* * *
```

from the beginning of the trace.

### Interpretation

This demonstrated that different traceroute probe types can produce different results.

It reinforced the principle:

> A traceroute result must be interpreted in the context of how the probes are handled by the network.

The TCP traceroute alone could not identify the exact failure point.



# 15. Failure — Deliberate Unreachable Destination

The remote destination was intentionally used as the failure scenario.

The expected behavior was:

```text
Host
 ↓
Default Gateway
 ↓
Upstream Network
 ↓
Remote Destination
```

The actual result was:

```text
Host
 ↓
Default Gateway       ✓
 ↓
Several Routers       ✓
 ↓
Unknown/Unresponsive Path
 ↓
Remote Destination    ✗
```

The failure was therefore useful because it created an opportunity to practice fault isolation.

---

# 16. Troubleshooting Process

The troubleshooting process followed an evidence-based sequence.

## Step 1 — Check the host

Questions:

* Does the interface exist?
* Does it have an IPv4 address?

Result:

```text
Yes
```

---

## Step 2 — Check the routing table

Question:

> Does the host have a route for the destination?

Result:

```text
No specific route
```

The default route was available.

---

## Step 3 — Check the next hop

Question:

> Can the host reach the gateway?

Result:

```text
Yes
```

---

## Step 4 — Check ARP

Question:

> Does the host know the gateway's MAC address?

Result:

```text
Yes
```

---

## Step 5 — Test the destination

Question:

> Does the destination respond?

Result:

```text
No
```

---

## Step 6 — Trace the path

Question:

> How far does traffic appear to travel?

Result:

```text
Multiple upstream routers responded.
```

---

# 17. Evidence Collected

The major evidence collected was:

### Host configuration

```text
Interface: en0
IPv4: <MASKED>
```

### Default route

```text
default → <MASKED_GATEWAY_IP>
```

### Gateway connectivity

```text
Ping → successful
```

### Gateway ARP

```text
<MASKED_GATEWAY_IP>
      ↓
<MASKED_GATEWAY_MAC>
```

### Destination route

```text
<MASKED_REMOTE_IP>
      ↓
default
      ↓
<MASKED_GATEWAY_IP>
```

### Destination ping

```text
100% packet loss
```

### Traceroute

```text
Multiple routers responding
```

This combination of evidence was much more useful than relying on ping alone.



# 18. Root Cause / Fault Domain

The exact root cause could not be proven from the host alone.

However, the evidence allowed the fault domain to be narrowed.

### Eliminated or weakened possibilities

```text
Local interface failure          → unlikely
Missing IPv4 address             → eliminated
Missing default route            → eliminated
Gateway unavailable              → unlikely
Gateway MAC unresolved           → eliminated
Local route-selection failure    → unlikely
```

### Remaining fault domain

```text
Beyond the local gateway
```

Possible causes include:

* Upstream routing problem
* Remote network unavailable
* Destination host unavailable
* Firewall filtering
* ICMP filtering
* Failure farther along the path

Therefore the correct professional conclusion was:

> The host's local routing and gateway connectivity appear healthy; the failure appears to be somewhere upstream or beyond the gateway.



# 19. Resolution

The exact upstream problem could not be repaired from the Mac because the investigation did not provide administrative access to the intermediate routers or remote network.

The appropriate resolution at the host level was therefore:

1. Confirm the local configuration.
2. Confirm the default gateway.
3. Confirm gateway connectivity.
4. Confirm the selected route.
5. Trace the path.
6. Narrow the fault domain.
7. Escalate the upstream fault with collected evidence.

This is an important troubleshooting outcome.

A network engineer does not always need to personally repair the fault to successfully troubleshoot it.

Sometimes the correct result is:

> "The fault has been isolated to a specific section of the network."



# 20. Security Considerations

Routing and path-analysis information can reveal network topology.

Information such as:

* Internal IP addresses
* Gateway addresses
* Router addresses
* MAC addresses
* Network ranges
* Traceroute paths

can provide useful information to an attacker during reconnaissance.

Therefore:

* Do not publicly expose real internal routing tables.
* Mask internal IP addresses in public documentation.
* Mask MAC addresses where unnecessary.
* Avoid publishing complete network topology.
* Treat diagnostic output as potentially sensitive infrastructure information.

This README therefore uses masked network information.



# 21. Automation Opportunities

The troubleshooting process could eventually be partially automated.

A script could collect:

```text
1. Interface status
2. IPv4 address
3. Default gateway
4. Routing table
5. Gateway ARP entry
6. Gateway ping
7. Destination ping
8. Route to destination
9. Traceroute
```

The script could then produce a report such as:

```text
Interface:             PASS
IPv4 configuration:    PASS
Default route:         PASS
Gateway reachability:  PASS
ARP resolution:        PASS
Destination reachability: FAIL
Traceroute:             PARTIAL
Likely fault domain:    UPSTREAM
```

This could later become a Python networking troubleshooting project.



# 22. Lessons Learned

## Lesson 1 — Ping failure is not enough

A failed ping does not prove that:

```text
The destination does not exist.
```

It only proves that the destination did not respond to the ICMP test.



## Lesson 2 — Troubleshoot from the bottom up

A useful sequence is:

```text
Interface
   ↓
IP configuration
   ↓
Local routing
   ↓
Gateway
   ↓
Upstream path
   ↓
Destination
```



## Lesson 3 — Use evidence to eliminate possibilities

Instead of saying:

> "The network is broken."

we can say:

> "The local interface, routing configuration and gateway connectivity have been verified. The remaining fault domain is upstream."

This is a much stronger technical conclusion.



## Lesson 4 — `* * *` does not automatically mean failure

It means:

> No response was received from that traceroute probe.

Additional investigation is required before declaring a router or network unavailable.



## Lesson 5 — Routing and ARP have different jobs

```text
Routing
   ↓
Determines next hop

ARP
   ↓
Determines local MAC address
```

These processes work together but solve different problems.



# 23. Practical Skills Acquired

## Routing skills

* Inspecting IPv4 routing tables
* Identifying default routes
* Determining selected routes
* Identifying next hops
* Identifying outgoing interfaces
* Understanding route selection during troubleshooting

## Layer 2 skills

* Inspecting ARP entries
* Connecting IP addresses to MAC addresses
* Understanding gateway MAC resolution

## Troubleshooting skills

* Building a troubleshooting baseline
* Testing local connectivity
* Testing gateway connectivity
* Testing remote connectivity
* Tracing a network path
* Interpreting traceroute
* Narrowing a fault domain
* Separating evidence from assumptions
* Escalating a problem with useful evidence

## Terminal skills

* `ipconfig`
* `route`
* `netstat`
* `arp`
* `ping`
* `traceroute`
* Combining commands during troubleshooting



# 24. Relationship With Previously Learned Foundation Skills

This lab combines several earlier networking concepts.

## IPv4 addressing

Previously learned:

```text
IP address
+
Prefix
=
Network membership
```

This allows us to determine whether a destination is local or remote.



## Ethernet and Layer 2

Previously learned:

* MAC addresses
* Ethernet frames
* Interfaces
* Switching

This lab adds:

```text
Routing decision
      ↓
Next hop
      ↓
ARP
      ↓
MAC address
      ↓
Layer 2 transmission
```



## ARP

Previously learned:

```text
IPv4 address
      ↕
MAC address
```

This lab reinforces that ARP is used for local Layer 2 delivery rather than deciding the IP route.

---

## Routing

Previously learned:

* Connected routes
* Default routes
* Specific routes
* Longest-prefix matching

This lab applies those concepts to real troubleshooting.


# 25. Connection to Intermediate Skills

The skills developed here directly prepare for:

## Static Routing

Later, manually configured routes will allow specific networks to be reached through specific next hops.

The troubleshooting process remains:

```text
Destination
   ↓
Route
   ↓
Next hop
   ↓
Interface
```

---

## Dynamic Routing

Protocols such as:

* OSPF
* RIP
* BGP

will introduce dynamically learned routes.

When something fails, the same reasoning applies:

> Which route was selected and why?

---

## Network Troubleshooting

These commands will become increasingly useful together:

```text
ping
traceroute
arp
route
netstat
tcpdump
```

Rather than using them independently, they become parts of a structured diagnostic process.

---

# 26. Connection to Advanced Skills

## Network Security

Routing-path knowledge will support:

* Firewall analysis
* Network segmentation
* Traffic analysis
* Security monitoring
* Reconnaissance analysis
* Attack-path analysis

---

## Cloud Networking

The same concepts appear in cloud environments:

```text
Virtual Network
      ↓
Subnet
      ↓
Route Table
      ↓
Next Hop
      ↓
Gateway
      ↓
Destination
```

---

## Automation

The troubleshooting workflow can eventually be converted into Python-based diagnostic tooling.

For example:

```text
Python
  ↓
Collect network state
  ↓
Analyze routes
  ↓
Test connectivity
  ↓
Trace path
  ↓
Generate diagnostic report
```

This connects networking fundamentals with future Python and automation skills.

---

# 27. Foundation → Intermediate → Advanced Skill Chain

```text
IPv4 Addressing
       ↓
Subnetting
       ↓
MAC Addresses
       ↓
Ethernet
       ↓
ARP
       ↓
Routing Tables
       ↓
Route Selection
       ↓
Routing Troubleshooting
       ↓
Static Routing
       ↓
Dynamic Routing
       ↓
OSPF / BGP
       ↓
Network Design
       ↓
Cloud Networking
       ↓
Network Security
       ↓
Advanced Troubleshooting
       ↓
Network Automation
```

This demonstrates that the lab is not an isolated exercise.

It connects Layer 2 knowledge to Layer 3 routing, troubleshooting, security, cloud and automation.

---

# 28. Final Troubleshooting Workflow

The most important workflow from this lab is:

```text
                Problem
                   ↓
          Check interface
                   ↓
        Check IPv4 configuration
                   ↓
          Check routing table
                   ↓
       Determine selected route
                   ↓
          Identify next hop
                   ↓
       Check ARP if applicable
                   ↓
        Test next-hop reachability
                   ↓
          Test destination
                   ↓
             Traceroute
                   ↓
          Analyze responding hops
                   ↓
       Eliminate confirmed-good areas
                   ↓
          Narrow fault domain
                   ↓
          Resolve or escalate
```

---

# 29. Final Takeaway

This lab moved routing knowledge from simple route selection into practical troubleshooting.

The most important lesson was not a particular command.

It was the ability to reason from evidence.

Instead of concluding:

> "The destination is down."

I learned to say:

> "The destination is not responding to my test, but the local interface, routing configuration and gateway connectivity have been verified. Traceroute shows the traffic reaching multiple upstream routers, so the fault domain appears to be beyond the local gateway."

The fundamental troubleshooting principle learned is:

```text
Don't guess where the problem is.

Collect evidence.

Eliminate what is known to work.

Narrow the remaining fault domain.

Then investigate further.
```

This provides the foundation for the next routing labs and for future work in network engineering, cloud networking, cybersecurity and network automation.
