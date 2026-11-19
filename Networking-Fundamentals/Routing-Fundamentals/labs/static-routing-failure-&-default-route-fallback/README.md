# Lab 5 — Static Routing: Configuration, Route Selection & Failure Analysis

## 1. Overview

This lab focused on understanding and implementing **static IPv4 routing** on a real macOS system.

The lab built on the route-selection concepts established in Lab 1 and demonstrated how a manually configured route can provide a more-specific forwarding instruction than the default route.

The lab also deliberately removed the static route to observe the resulting change in route selection and to practice a structured troubleshooting process.

The lab was performed using the host's actual IPv4 routing table rather than a simulated environment.


# 2. Scenario — Problem Being Solved

A host needs to communicate with a remote IPv4 network.

The host already has a default route, but an administrator wants traffic destined for a particular remote network to have an explicitly defined route.

The problem being investigated was:

> How can a host be instructed to use a specific route for a particular destination network, and what happens if that route is removed?

The lab therefore demonstrated:

* Static route creation
* Specific route selection
* Default-route fallback
* Route verification
* Deliberate route failure
* Troubleshooting using routing-table evidence



# 3. Architecture

The practical topology was conceptually:

```text
                  macOS Host
              ┌───────────────┐
              │   IPv4 Host   │
              │               │
              │ Interface:    │
              │ en0           │
              └───────┬───────┘
                      │
                      │ Local network
                      │
              ┌───────▼───────┐
              │ Default/Next  │
              │ Hop Router    │
              └───────┬───────┘
                      │
                      │
                Remote Network
                10.20.30.0/24
                      │
                      ▼
              Remote Destination
                10.20.30.50
```

### Components involved

* macOS host
* `en0` network interface
* Local IPv4 network
* Default gateway
* Remote destination network
* IPv4 routing table
* Static route
* Default route

The actual environment-specific IP addresses and MAC addresses have been intentionally masked.


# 4. Objectives

By completing this lab, I aimed to learn how to:

* Understand what a static route is
* Add a static route from the terminal
* Identify the destination network of a static route
* Identify the next-hop gateway
* Understand how static routes interact with default routes
* Apply longest-prefix matching
* Verify a static route using the routing table
* Determine the route selected for a particular destination
* Deliberately remove a static route
* Observe default-route fallback
* Collect troubleshooting evidence
* Identify the root cause of a routing problem
* Understand why a default route does not necessarily provide the intended path
* Connect static routing with practical network administration


# 5. Environment

| Item                     | Details               |
| ------------------------ | --------------------- |
| Device                   | Mac                   |
| Operating System         | macOS                 |
| Network Interface        | `en0`                 |
| Connection               | Wi-Fi                 |
| Addressing               | IPv4                  |
| Primary routing command  | `netstat -rn -f inet` |
| Route inspection command | `route -n get`        |

Environment-specific addressing has been masked where appropriate.


# 6. Important Concepts

## 6.1 Static Route

A static route is a route that has been manually configured by an administrator.

Conceptually:

```text
Destination Network
        ↓
Next Hop
        ↓
Outgoing Interface
```

Example used in this lab:

```text
10.20.30.0/24
        ↓
192.168.100.1
        ↓
en0
```

The addresses above are retained only as lab examples; environment-specific information should be masked before public publication.



# 7. Default Route

The host already had a default route:

```text
default → [MASKED_GATEWAY]
```

A default route represents:

```text
0.0.0.0/0
```

It is used when no more-specific route matches the destination.

The important distinction is:

```text
Specific route
      ↓
Used when it matches

Default route
      ↓
Fallback when no more-specific route matches
```

# 8. Understanding the Destination

The destination host used during the lab was:

```text
10.20.30.50
```

This host belongs to:

```text
10.20.30.0/24
```

Here:

```text
10.20.30.0 = Network address
/24          = Prefix length
10.20.30.50  = Destination host
```

The route therefore describes how to reach the **network**, while the packet itself can be destined for a particular host within that network.



# 9. Initial Routing State

The routing table initially contained a default route.

Conceptually:

```text
default → [MASKED_GATEWAY] → en0
```

There was initially no specific route for:

```text
10.20.30.0/24
```

Therefore, when the host was asked how to reach:

```text
10.20.30.50
```

the default route was selected.



# 10. Command — Inspect the Routing Table

```bash
netstat -rn -f inet
```

### Use

Displays the host's IPv4 routing table.

It allows the administrator to identify:

* Connected networks
* Static routes
* Default routes
* Gateways
* Interfaces
* Host-specific routes



# 11. Command — Determine the Route to a Destination

```bash
route -n get 10.20.30.50
```

### Use

Shows the specific route macOS selects when attempting to reach:

```text
10.20.30.50
```

This is particularly useful because it reveals the actual forwarding decision rather than requiring the administrator to infer it only from the routing table.


# 12. Initial Route Selection

Before configuring the static route, the host selected:

```text
destination: default
mask:        default
gateway:     [MASKED_GATEWAY]
interface:   en0
```

This demonstrated that:

```text
10.20.30.50
      ↓
No specific route
      ↓
Use default route
      ↓
[MASKED_GATEWAY]
      ↓
en0
```



# 13. Implementation — Adding the Static Route

The static route was manually configured using:

```bash
sudo route -n add -net 10.20.30.0/24 [MASKED_GATEWAY]
```

### Use

Adds a manually configured route for:

```text
10.20.30.0/24
```

using the specified next-hop gateway.

The resulting routing instruction is conceptually:

```text
10.20.30.0/24
        ↓
[MASKED_GATEWAY]
        ↓
en0
```



# 14. Verification — Static Route Appears

The routing table was then inspected using:

```bash
netstat -rn -f inet
```

The resulting table contained an entry equivalent to:

```text
10.20.30/24    [MASKED_GATEWAY]    UGSc    en0
```

This provided evidence that the static route had been successfully installed.



# 15. Verification — Route Selection

The following command was used:

```bash
route -n get 10.20.30.50
```

### Result

The system reported:

```text
route to: 10.20.30.50

destination: 10.20.30.0
mask:        255.255.255.0
gateway:     [MASKED_GATEWAY]
interface:   en0
```

This was significant because the selected destination was no longer reported as the default route.

Instead, macOS selected:

```text
10.20.30.0/24
```



# 16. Why the Static Route Won

The destination:

```text
10.20.30.50
```

matched:

```text
10.20.30.0/24
```

It also technically matched:

```text
0.0.0.0/0
```

because the default route matches every IPv4 destination.

However:

```text
/24
```

is more specific than:

```text
/0
```

Therefore:

```text
10.20.30.0/24
        ↓
wins
        ↓
0.0.0.0/0
```

This demonstrated **longest-prefix matching** in practice.



# 17. Important Distinction — Route vs Destination

One of the important concepts clarified during this lab was the difference between:

* Destination host
* Destination network
* Route
* Next hop

For example:

```text
Destination host:
10.20.30.50

Destination network:
10.20.30.0/24

Next hop:
[MASKED_GATEWAY]

Interface:
en0
```

A route can therefore be understood as a forwarding instruction:

```text
10.20.30.0/24
        ↓
[MASKED_GATEWAY]
        ↓
en0
```

The route does not mean that `10.20.30.0` is the individual device being contacted.

`10.20.30.0` is the network address.



# 18. Test — Unrelated Destination

The destination:

```text
10.20.40.50
```

was tested.

The specific static route:

```text
10.20.30.0/24
```

does not match this destination.

Therefore, the default route remained the selected route.

The command used was:

```bash
route -n get 10.20.40.50
```

### Use

Determines which routing-table entry macOS selects for an unrelated destination.

### Result

Conceptually:

```text
10.20.40.50
      ↓
10.20.30.0/24 does not match
      ↓
Default route matches
      ↓
[MASKED_GATEWAY]
      ↓
en0
```

This demonstrated that a static route only affects destinations within its defined prefix.



# 19. Deliberate Failure

To understand what happens when a static route disappears, the route was deliberately removed.

Command:

```bash
sudo route -n delete -net 10.20.30.0/24
```

### Use

Removes the manually configured static route for:

```text
10.20.30.0/24
```

This was the deliberate failure introduced for the lab.



# 20. Failure Verification

After removing the static route, the routing table was inspected again:

```bash
netstat -rn -f inet
```

### Evidence

The following entry was no longer present:

```text
10.20.30/24
```

The default route remained:

```text
default → [MASKED_GATEWAY]
```

This confirmed that the specific route had actually been removed.


# 21. Failure — Route Selection After Removal

The following command was then executed:

```bash
route -n get 10.20.30.50
```

### Result

The system returned:

```text
route to: 10.20.30.50

destination: default
mask:        default
gateway:     [MASKED_GATEWAY]
interface:   en0
```

This demonstrated that the host had fallen back to the default route.

The forwarding decision therefore changed from:

```text
10.20.30.50
      ↓
10.20.30.0/24
      ↓
[MASKED_GATEWAY]
```

to:

```text
10.20.30.50
      ↓
No specific route
      ↓
Default route
      ↓
[MASKED_GATEWAY]
```



# 22. Troubleshooting — Evidence Collected

The troubleshooting process relied on observable system evidence.

### Evidence 1 — Routing table before configuration

```bash
netstat -rn -f inet
```

Confirmed that no specific route for the target network existed.

### Evidence 2 — Route selection before configuration

```bash
route -n get 10.20.30.50
```

Confirmed that the default route was selected.

### Evidence 3 — Routing table after configuration

```bash
netstat -rn -f inet
```

Confirmed the presence of:

```text
10.20.30/24 → [MASKED_GATEWAY]
```

### Evidence 4 — Route selection after configuration

```bash
route -n get 10.20.30.50
```

Confirmed selection of:

```text
10.20.30.0/24
```

### Evidence 5 — Routing table after deliberate failure

Confirmed that the static route had disappeared.

### Evidence 6 — Route selection after failure

Confirmed that:

```text
default
```

was selected instead.

This sequence provided objective evidence rather than relying on assumptions.



# 23. Root Cause

The deliberate routing failure occurred because the specific static route for:

```text
10.20.30.0/24
```

was removed.

Once the route disappeared, the host had no more-specific routing-table entry for the destination.

Therefore, the operating system selected:

```text
0.0.0.0/0
```

the default route.

### Root cause

> The specific route required for the intended forwarding decision was absent from the routing table.



# 24. Resolution

The resolution was to restore the static route:

```bash
sudo route -n add -net 10.20.30.0/24 [MASKED_GATEWAY]
```

### Use

Restores the manually configured route for the target network.

The route can then be verified using:

```bash
netstat -rn -f inet
```

and:

```bash
route -n get 10.20.30.50
```

The expected result is that:

```text
10.20.30.0/24
```

is selected instead of:

```text
default
```



# 25. Important Troubleshooting Lesson

A default route does not guarantee that traffic will follow the intended path.

If a specific route disappears:

```text
Specific route
      ↓
missing
      ↓
Default route
      ↓
Fallback path
```

The traffic may:

* Still reach the destination
* Follow a different path
* Be forwarded to a router that does not know the destination
* Eventually fail

Therefore:

> A working default route does not prove that the correct route exists.


# 26. Security Considerations

Incorrect static routes can create security and operational problems.

Potential risks include:

### Traffic following an unintended path

A missing or incorrect route can cause traffic to pass through an unexpected router.

### Traffic interception

If traffic is deliberately or accidentally redirected through an untrusted network device, sensitive traffic could potentially be exposed.

### Network isolation bypass

Incorrect routing can undermine intended network segmentation.

### Connectivity failures

Incorrect routes can make legitimate services unreachable.

### Administrative mistakes

Manually configured routes can become outdated when network architecture changes.

Static routing therefore requires careful documentation and verification.



# 27. Automation Opportunities

Static route management can potentially be automated in larger environments.

Examples include:

* Scripts that verify required routes
* Configuration-management systems
* Network monitoring tools
* Automated route validation
* Startup scripts that restore required routes
* Alerting when expected routes disappear

A simple automated check could conceptually verify:

```text
Required route exists?
        ↓
YES → continue
NO  → alert administrator
```

Automation should be used carefully because automatically changing routing configuration without validation can create larger connectivity problems.



# 28. Lessons Learned

The main lessons from this lab were:

### 1. A static route is a forwarding instruction

It tells the host how to reach a particular destination network.

### 2. The destination host and destination network are different

For example:

```text
10.20.30.50
```

is the destination host.

```text
10.20.30.0/24
```

is the destination network.

### 3. The default route is a fallback

```text
0.0.0.0/0
```

matches destinations when no more-specific route is available.

### 4. More-specific routes win

```text
10.20.30.0/24
```

wins over:

```text
0.0.0.0/0
```

when both match.

### 5. Removing a route changes the forwarding decision

The destination itself does not change.

The available routing instructions change.

### 6. Troubleshooting should be evidence-driven

Instead of assuming what the host is doing, commands such as:

```bash
netstat -rn -f inet
```

and:

```bash
route -n get <destination>
```

can reveal the actual forwarding decision.

### 7. A default route does not necessarily mean the correct path exists

It only provides a fallback forwarding instruction.



# 29. Practical Skills Demonstrated

After completing this lab, I can:

* Identify a default route
* Explain `0.0.0.0/0`
* Explain a destination network
* Configure a static route
* Remove a static route
* Verify routing-table changes
* Determine the route selected for a destination
* Apply longest-prefix matching
* Identify the next hop
* Identify the outgoing interface
* Deliberately create a routing failure
* Collect routing evidence
* Identify the root cause of a route-selection problem
* Restore the intended route
* Explain the operational and security implications of incorrect routing



# 30. Foundation-to-Advanced Connection

The concepts demonstrated in this lab form the foundation for later networking skills:

```text
IPv4 Addressing
       ↓
Subnetting
       ↓
Routing Tables
       ↓
Route Selection
       ↓
Static Routing
       ↓
Multiple Routes
       ↓
Dynamic Routing
       ↓
OSPF
       ↓
BGP
       ↓
Network Design
       ↓
Cloud Routing
       ↓
Network Security
       ↓
Advanced Troubleshooting
```

The same fundamental question continues to apply:

> **Which route should be used to reach this destination?**



# 31. Connection to Cybersecurity

Static routing and route selection are also relevant to cybersecurity because security professionals need to understand where traffic travels.

Routing knowledge contributes to understanding:

* Network segmentation
* Traffic paths
* Security boundaries
* Firewall placement
* Network reconnaissance
* Traffic analysis
* Attack paths
* Routing-based misconfigurations
* Cloud network security

The cybersecurity applications will be studied later, but this lab establishes the underlying networking knowledge required to understand them.



# 32. Final Practical Workflow

The complete workflow developed in this lab can be summarized as:

```text
Destination IP
      ↓
Inspect routing table
      ↓
Find matching routes
      ↓
Is there a specific route?
      │
   ┌──┴──┐
  YES    NO
   ↓      ↓
Use most  Use default
specific  route
route
   │      │
   └──┬───┘
      ↓
Determine next hop
      ↓
Determine interface
      ↓
Proceed with Layer 2 delivery
```


# 33. Lab Evidence Summary

The practical evidence demonstrated the following progression:

### Before static route

```text
10.20.30.50
      ↓
default
      ↓
[MASKED_GATEWAY]
```

### After static route

```text
10.20.30.50
      ↓
10.20.30.0/24
      ↓
[MASKED_GATEWAY]
```

### After deliberate removal

```text
10.20.30.50
      ↓
default
      ↓
[MASKED_GATEWAY]
```

This provided direct practical evidence of route selection and default-route fallback.


# 34. Conclusion

This lab moved static routing from theory into practical host-level configuration and troubleshooting.

I learned that a static route provides a **specific forwarding instruction** for a destination network.

I also demonstrated that a destination can match both a specific route and the default route, but the more-specific route wins through longest-prefix matching.

The practical process was:

```text
Configure
   ↓
Verify
   ↓
Test
   ↓
Deliberately break
   ↓
Collect evidence
   ↓
Identify root cause
   ↓
Restore configuration
   ↓
Verify again
```

The most important distinction established in this lab is:

> **The destination host does not change when a route is removed; the routing-table instruction used to reach that destination changes.**

This provides the foundation for the next routing labs involving multiple routes, route selection, and more advanced routing behavior.
