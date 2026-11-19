# Lab 3 — Static Routes

## Overview

This lab focused on understanding and practically demonstrating **static routing** at the host level.

The lab was performed on a real macOS system using the terminal and the host's actual routing table. A safe test network was used so that the experiment could be performed without disrupting normal Internet connectivity.

The lab moved beyond simply defining a static route and demonstrated:

* Creating a static route
* Inspecting the route in the routing table
* Verifying which route macOS selects for a destination
* Comparing a specific static route with the default route
* Deliberately removing the static route
* Observing the resulting change in route selection
* Restoring the route
* Connecting static routing to previously learned IPv4, subnetting, ARP, Layer 2, and routing-table concepts



# 1. Scenario — Problem Being Solved

A host may know how to reach its directly connected network and may have a default route for general traffic, but sometimes a specific path to another network needs to be manually defined.

The problem investigated in this lab was:

> **How can a specific destination network be given a manually defined next hop?**

A static route provides an explicit instruction such as:

```text
10.20.30.0/24 → <NEXT-HOP-IP>
```

Meaning:

> To reach the `10.20.30.0/24` network, send traffic to the specified next-hop router.



# 2. Architecture

The practical test used the following conceptual architecture:

```text
                    macOS Host
                        │
                        │ en0
                        │
                 Local Network
                        │
                        │
                 <TEST GATEWAY>
                        │
                        │
                 <TEST NETWORK>
                  10.20.30.0/24
```

The test did not require a real device to exist inside the destination network because the objective was to verify **route selection**, not end-to-end connectivity.

The important components were:

* macOS host
* `en0` network interface
* Local IPv4 network
* Existing default gateway
* Static route
* Destination test network
* Routing table



# 3. Objectives

By completing this lab, I aimed to learn how to:

* Understand what a static route is
* Understand why static routes are used
* Identify a destination network
* Identify a next-hop IP address
* Create a static route from the terminal
* Verify a static route in the routing table
* Use `route -n get` to determine the selected route
* Distinguish a specific route from a default route
* Understand what the `STATIC` flag indicates
* Deliberately remove a static route
* Observe the resulting change in route selection
* Restore the static route
* Connect static routing with previously learned routing fundamentals



# 4. Environment

| Item                  | Details               |
| --------------------- | --------------------- |
| Device                | Mac                   |
| Operating System      | macOS                 |
| Network Interface     | `en0`                 |
| Connection            | Wi-Fi                 |
| Addressing            | IPv4                  |
| Terminal              | macOS Terminal        |
| Routing table command | `netstat -rn -f inet` |
| Route lookup command  | `route -n get`        |

Actual IP addresses and MAC addresses from the real network have been intentionally masked in this documentation.



# 5. Commands Used

### Inspect routing table

```bash
netstat -rn -f inet
```

Used to display the host's IPv4 routing table.

### Inspect a specific route

```bash
route -n get <DESTINATION-IP>
```

Used to determine which route macOS selects for a particular destination.

### Add a static route

```bash
sudo route -n add -net <DESTINATION-NETWORK>/24 <NEXT-HOP-IP>
```

### Delete a static route

```bash
sudo route -n delete -net <DESTINATION-NETWORK>/24 <NEXT-HOP-IP>
```



# 6. Initial Routing State

Before creating the test route, the host already had:

```text
default → <DEFAULT-GATEWAY>
```

and a directly connected local network.

This meant that the host already knew how to:

1. Reach its local network directly.
2. Send traffic for destinations without a more-specific route toward the default gateway.

The static-route experiment introduced an additional, more-specific route.



# 7. Static Route Concept

The test route represented:

```text
<TEST-NETWORK>/24 → <NEXT-HOP>
```

The important structure is:

```text
DESTINATION NETWORK → NEXT HOP
```

For example:

```text
10.20.30.0/24 → <NEXT-HOP>
```

means:

> To reach the `10.20.30.0/24` network, forward the traffic toward the specified next-hop IP.

A static route is called **static** because it is manually configured rather than dynamically learned through a routing protocol.



# 8. Implementation

The static route was added using:

```bash
sudo route -n add -net <TEST-NETWORK>/24 <NEXT-HOP-IP>
```

The command successfully created an entry representing:

```text
<TEST-NETWORK>/24 → <NEXT-HOP>
```

The route was then visible in the routing table.

Conceptually:

```text
Destination        Gateway        Interface
------------------------------------------------
<TEST-NETWORK>/24  <NEXT-HOP>     en0
```



# 9. Verification

The routing table was inspected with:

```bash
netstat -rn -f inet
```

The new static route appeared in the routing table.

A destination inside the test network was then selected:

```text
<TEST-HOST-IP>
```

The route was inspected using:

```bash
route -n get <TEST-HOST-IP>
```

The output showed:

```text
destination: <TEST-NETWORK>
mask:        255.255.255.0
gateway:     <NEXT-HOP>
interface:   en0
flags:       ... STATIC ...
```

This provided direct evidence that macOS was selecting the static route.



# 10. Understanding the Route Lookup

An important observation was that the route lookup was performed against a **host IP**, while the result identified the **network route**.

For example:

```text
Requested destination:

<TEST-HOST-IP>
```

The routing table returned:

```text
destination:

<TEST-NETWORK>
```

with:

```text
mask:

255.255.255.0
```

This demonstrates that the route applies to the entire `/24` network rather than to one individual host.

Therefore, a route such as:

```text
10.20.30.0/24
```

can match:

```text
10.20.30.1
10.20.30.10
10.20.30.50
10.20.30.200
```

but not:

```text
10.20.40.10
```



# 11. Static Route vs Default Route

At the same time, the routing table contained both:

```text
<TEST-NETWORK>/24 → <NEXT-HOP>
```

and:

```text
default → <DEFAULT-GATEWAY>
```

These routes have different purposes.

### Specific route

```text
<TEST-NETWORK>/24
```

means:

> Traffic for this particular network follows this route.

### Default route

```text
0.0.0.0/0
```

means:

> If no more-specific route matches, use this route.

Therefore:

```text
Destination
     ↓
Does specific route match?
     ↓
YES → use specific route

NO
     ↓
Use default route
```

---

# 12. Test — Specific Destination

A destination inside the test network was examined.

Conceptually:

```text
Destination:
<TEST-NETWORK host>

        ↓

Does <TEST-NETWORK>/24 match?

        ↓

YES

        ↓

Use static route

        ↓

Next hop:
<NEXT-HOP>
```

The route lookup confirmed that the specific static route was selected.

---

# 13. Test — Destination Outside the Static Route

A destination outside the test network was then considered.

For example:

```text
8.8.8.8
```

The static route:

```text
<TEST-NETWORK>/24
```

does not match that destination.

Therefore:

```text
Specific route?
      ↓
     NO
      ↓
Default route
      ↓
<DEFAULT-GATEWAY>
```

This demonstrated that a static route does not replace the default route.

Instead, the static route provides a **more-specific path for a particular destination network**.

---

# 14. Deliberate Failure

The static route was deliberately removed using:

```bash
sudo route -n delete -net <TEST-NETWORK>/24 <NEXT-HOP-IP>
```

The routing table was then checked again.

The specific static route was no longer present.

A route lookup was performed for a destination that previously matched the static route.

---

# 15. Failure Evidence

Before removing the static route:

```text
destination: <TEST-NETWORK>
mask:        255.255.255.0
gateway:     <NEXT-HOP>
interface:   en0
flags:       STATIC
```

After removing it:

```text
destination: default
mask:        default
gateway:     <DEFAULT-GATEWAY>
interface:   en0
```

This was one of the most important observations in the lab.

The destination did not change.

What changed was the **route selected to reach that destination**.

---

# 16. Troubleshooting

The troubleshooting process was based on evidence from the routing table.

### Evidence collected

```bash
netstat -rn -f inet
```

was used to determine whether the static route existed.

Then:

```bash
route -n get <DESTINATION-IP>
```

was used to determine which route macOS would actually select.

This provided two different types of evidence:

### Routing table evidence

Answers:

> What routes currently exist?

### Route lookup evidence

Answers:

> Which route will be selected for this particular destination?

---

# 17. Root Cause of the Failure

The deliberate failure occurred because the static route was removed.

Before removal:

```text
<TEST-NETWORK>/24 → <NEXT-HOP>
```

After removal:

```text
Specific route → absent
```

The destination therefore no longer had a specific matching route.

Because the host still had a default route, the destination fell back to:

```text
default → <DEFAULT-GATEWAY>
```

The root cause was therefore:

> **The specific static route no longer existed in the routing table.**

---

# 18. Resolution

The static route was restored using:

```bash
sudo route -n add -net <TEST-NETWORK>/24 <NEXT-HOP-IP>
```

The route was then verified again using:

```bash
route -n get <TEST-HOST-IP>
```

The output once again showed:

```text
destination: <TEST-NETWORK>
mask:        255.255.255.0
gateway:     <NEXT-HOP>
interface:   en0
flags:       STATIC
```

This confirmed that the specific route had been restored.

---

# 19. Important Lesson From the Failure

The failure demonstrated an important troubleshooting principle:

> **Do not assume that the default gateway being present means the correct route is being used.**

A host can have:

* A working network interface
* An IPv4 address
* A default gateway
* Internet connectivity

and still have an incorrect or missing route for a particular network.

Therefore, troubleshooting should include:

```text
Check interface
      ↓
Check IP address
      ↓
Check routing table
      ↓
Check route for destination
      ↓
Identify selected next hop
      ↓
Investigate Layer 2 delivery if necessary
```

---

# 20. Security Considerations

Static routes can affect where traffic travels.

If a malicious or unauthorized person gains the ability to modify routing information, traffic could potentially be redirected through an unintended device.

Possible risks include:

* Traffic interception
* Traffic redirection
* Loss of connectivity
* Incorrect network access
* Routing loops
* Bypassing intended network paths
* Exposure of sensitive traffic

At this foundational level, the important security lesson is:

> **Routing information is part of the security boundary because it determines where traffic is sent.**

Later networking and cybersecurity studies will build on this concept.

---

# 21. Automation Possibilities

Static route configuration can potentially be automated when the same network configuration must be deployed repeatedly.

Possible automation tasks include:

* Adding predefined routes
* Removing obsolete routes
* Checking whether expected routes exist
* Comparing current routes against an expected configuration
* Alerting when routes change
* Generating routing configuration from infrastructure data

At the automation stage, these tasks could eventually be performed using:

```text
Shell scripting
        ↓
Python
        ↓
Configuration automation
        ↓
Infrastructure automation
```

The current lab provides the conceptual knowledge required before automating such tasks.

---

# 22. Skills Actually Learned

### Routing skills

* Understand what a static route is
* Identify a destination network
* Identify a next-hop IP
* Create a static route
* Delete a static route
* Verify a static route
* Understand the `STATIC` route flag
* Distinguish a specific route from a default route
* Understand route fallback to the default route

### Troubleshooting skills

* Inspect the routing table
* Perform destination-specific route lookups
* Compare routing behavior before and after a configuration change
* Deliberately introduce a routing failure
* Identify the missing route as the root cause
* Restore the expected route

### Terminal skills

* Use `netstat -rn -f inet`
* Use `route -n get`
* Use `sudo route -n add`
* Use `sudo route -n delete`

---

# 23. Connection With Previously Learned Foundations

This lab builds directly on previous networking knowledge.

## IPv4 Addressing

Previously learned:

```text
IP address
Network portion
Host portion
Prefix length
```

This lab applied those concepts to:

```text
<TEST-NETWORK>/24
```

The `/24` determines which destinations belong to the route.

---

## Subnetting

Previously learned how a prefix determines network boundaries.

This lab applied that knowledge when determining whether a destination belongs to:

```text
<TEST-NETWORK>/24
```

For example:

```text
10.20.30.x → belongs to the network

10.20.40.x → does not
```

---

## Network Interfaces

Previously learned that a network interface provides the connection between the host and network.

This lab showed that the routing decision also identifies an outgoing interface:

```text
Route
 ↓
en0
```

---

## ARP

Previously learned:

```text
IPv4 address → MAC address
```

through ARP.

This lab adds an important step before ARP:

```text
Destination IP
      ↓
Routing decision
      ↓
Next hop
      ↓
ARP if MAC resolution is required
      ↓
Layer 2 delivery
```

Routing therefore determines **who should receive the packet next**, while ARP can determine the MAC address required for local delivery.

---

## Ethernet and Layer 2

Previously learned:

* MAC addresses
* Ethernet frames
* Destination MAC
* Source MAC
* Switching

This lab connects those concepts to Layer 3:

```text
Layer 3
Routing
   ↓
Next hop
   ↓
Layer 2
MAC resolution
   ↓
Frame transmission
```

---

# 24. Connection to Future Intermediate Skills

## Advanced Static Routing

Later, static routes will be configured on actual routers and Layer 3 devices rather than only observing host routing behavior.

The fundamental structure remains:

```text
Destination network
        ↓
Next hop
        ↓
Outgoing interface
```

---

## Dynamic Routing

Later technologies such as:

* OSPF
* BGP
* RIP

will allow routers to learn routes dynamically.

The difference is primarily **how routes are learned**.

Static routing:

```text
Administrator
      ↓
Manual route
```

Dynamic routing:

```text
Routing protocol
      ↓
Learn route
```

The route-selection concepts learned here remain relevant.

---

## Network Troubleshooting

These commands and concepts will later be combined with:

```text
ping
traceroute
arp
tcpdump
netstat
route
```

to determine where network communication is failing.

---

## Cloud Networking

Cloud environments also use routing tables.

The same fundamental concept appears:

```text
Destination network
        ↓
Route
        ↓
Next hop / target
        ↓
Traffic forwarding
```

Therefore, host routing fundamentals provide a foundation for understanding cloud route tables later.

---

# 25. Connection to Future Cybersecurity Skills

Routing knowledge will eventually support cybersecurity activities such as:

* Network reconnaissance
* Traffic analysis
* Firewall analysis
* Network segmentation analysis
* Attack-path analysis
* Security monitoring
* Penetration testing

For example, understanding routes helps answer:

> Where can traffic travel?

> Which network does a host have access to?

> Through which gateway does traffic leave?

> Where could traffic potentially be redirected?

These questions become increasingly important in network security.

---

# 26. Practical Workflow Learned

The core workflow from this lab is:

```text
              Destination IP
                    ↓
            Inspect routing table
                    ↓
          Does a specific route match?
                /          \
              YES           NO
               ↓             ↓
       Use specific route   Default route
               ↓             ↓
             Next hop       Next hop
                \            /
                 ↓          ↓
                 Interface
                     ↓
              Need MAC address?
                     ↓
                    ARP
                     ↓
              Layer 2 delivery
```

---

# 27. Static Route Mental Model

The most useful mental model from this lab is:

```text
STATIC ROUTE

"For this particular network,
send traffic this way."
```

For example:

```text
10.20.30.0/24 → <NEXT-HOP>
```

means:

> **For traffic destined for 10.20.30.0/24, use the specified next hop.**

Whereas:

```text
default → <DEFAULT-GATEWAY>
```

means:

> **If no more-specific route matches, use the default gateway.**

---

# 28. Foundation-to-Advanced Skill Chain

The progression is:

```text
Network Interfaces
        ↓
IPv4 Addressing
        ↓
Subnetting
        ↓
MAC Addresses
        ↓
Ethernet
        ↓
Switching
        ↓
ARP
        ↓
Routing Tables
        ↓
Route Selection
        ↓
Static Routing
        ↓
Default Routing
        ↓
Longest-Prefix Matching
        ↓
Multi-Network Routing
        ↓
Dynamic Routing
        ↓
OSPF / Other Routing Protocols
        ↓
Network Design
        ↓
Cloud Networking
        ↓
Network Security
        ↓
Advanced Troubleshooting
```

Lab 3 therefore represents the transition from simply **reading routing information** to actually **creating and manipulating a route**.

---

# 29. Evidence of Practical Work

The lab produced practical evidence through:

### Routing table inspection

```bash
netstat -rn -f inet
```

showed the static route after configuration.

### Destination-specific lookup

```bash
route -n get <TEST-HOST-IP>
```

showed:

```text
destination: <TEST-NETWORK>
mask:        255.255.255.0
gateway:     <NEXT-HOP>
interface:   en0
STATIC
```

### Deliberate failure

After removing the static route, the same destination lookup selected:

```text
default
```

### Resolution

After restoring the route, the lookup again selected:

```text
<TEST-NETWORK>/24
```

This provided evidence that the routing behavior changed directly in response to the configuration.

---

# 30. Lessons — What I Actually Learned

The most important lessons from this lab were:

1. A static route is manually configured.
2. A route has a destination and a path toward that destination.
3. The destination network is not the same thing as the next-hop IP.
4. A `/24` route covers hosts within that specific network, not neighboring networks.
5. A specific route can take precedence over the default route.
6. If a specific route does not exist, the default route can be used.
7. Removing a route can change the selected path without changing the destination.
8. `route -n get` is useful for answering the practical question:

   > "Which route will my computer actually use?"
9. Routing happens before local Layer 2 delivery and possible ARP resolution.
10. Routing-table inspection is a practical troubleshooting skill, not merely a theoretical exercise.

---

# 31. Final Practical Summary

This lab demonstrated the complete lifecycle of a basic static route:

```text
                 Identify destination
                         ↓
                 Define destination
                       network
                         ↓
                  Define next hop
                         ↓
                  Add static route
                         ↓
                  Verify route
                         ↓
               Test route selection
                         ↓
              Deliberately remove it
                         ↓
                 Observe failure
                         ↓
              Identify missing route
                         ↓
                  Restore route
                         ↓
                  Verify again
```

The most important distinction established in this lab is:

> **A static route is a manually configured path to a specific destination network, while a default route is the fallback path used when no more-specific route matches.**

This provides the foundation for the next routing labs involving default routes, route selection, multi-network routing, and troubleshooting.
