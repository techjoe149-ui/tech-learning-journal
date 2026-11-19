# Lab 7 & 8 — Next-Hop Reasoning, Path Analysis & Reachability Troubleshooting

## 1. Overview

This lab combined two closely related routing skills:

* Understanding the **next hop** selected by the host
* Using path and reachability tests to determine **where a connectivity problem may exist**

The lab built on the static routing and longest-prefix matching concepts established in the previous labs.

The practical investigation followed traffic from the local macOS host toward a remote destination and compared:

* Routing-table information
* Selected next hop
* Interface
* Intermediate network hops
* Final destination reachability

The lab demonstrated how routing information and connectivity testing can be combined during network troubleshooting.


# 2. Scenario — Problem Being Solved

A host needs to communicate with a remote destination, but the destination does not respond to a connectivity test.

The problem being investigated was:

> If the local host can reach its gateway and traffic can progress through several network hops, but the final destination does not respond, where should troubleshooting continue?

The lab therefore demonstrated:

* Next-hop identification
* Route verification
* Gateway reachability testing
* Path discovery
* Destination reachability testing
* Failure localization
* Differentiating between evidence and assumptions


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
                      │
              ┌───────▼───────┐
              │ Local Gateway │
              └───────┬───────┘
                      │
                      ▼
                 Remote Routers
                 ┌────┴────┐
                 │         │
                 ▼         ▼
              Router     Router
                 │
                 ▼
          Remote Network
                 │
                 ▼
        Remote Destination

```

The actual gateway, host, and network addresses have been masked for publication.



# 4. Objectives

By completing this lab, I aimed to learn how to:

* Identify the next hop for a destination
* Identify the outgoing interface
* Verify the selected route
* Test gateway reachability
* Trace the path toward a remote destination
* Test final destination reachability
* Compare intermediate-hop responses with destination responses
* Localize a connectivity problem
* Avoid assuming that intermediate responses prove final reachability
* Identify possible causes of remote connectivity failure
* Apply a structured troubleshooting process

# 5. Environment

| Item                     | Details               |
| ------------------------ | --------------------- |
| Device                   | Mac                   |
| Operating System         | macOS                 |
| Network Interface        | `en0`                 |
| Connection               | Wi-Fi                 |
| Addressing               | IPv4                  |
| Routing-table command    | `netstat -rn -f inet` |
| Route inspection command | `route -n get`        |
| Reachability command     | `ping`                |
| Path-analysis command    | `traceroute`          |

Environment-specific IP addresses and MAC addresses have been masked where appropriate.



# 6. Important Concepts

## 6.1 Next Hop

The **next hop** is the router or gateway to which the host forwards traffic when the destination is not directly reachable on the local network.

Conceptually:

```text
Host
  ↓
Next Hop
  ↓
Other Routers
  ↓
Destination
```

The routing table determines the next hop based on the selected route.


# 7. Route Selection Before Testing

The route toward the remote destination was inspected using:

```bash
route -n get [REMOTE_DESTINATION]
```

The result identified:

```text
destination: [SELECTED_NETWORK]
mask:        [SELECTED_MASK]
gateway:     [MASKED_GATEWAY]
interface:   en0
```

This provided evidence of:

* The selected route
* The next-hop gateway
* The outgoing interface

The important relationship was:

```text
Destination
     ↓
Selected route
     ↓
Next-hop gateway
     ↓
en0
```



# 8. Test 1 — Gateway Reachability

The local gateway was tested using:

```bash
ping -c 4 [MASKED_GATEWAY]
```

### Use

Determines whether the host can communicate with its immediate next hop.

The test was successful.

Conceptually:

```text
Mac
 │
 ▼
Gateway
 │
 ✅
```

This provided evidence that the local host could reach its gateway.



# 9. What Gateway Reachability Proves

A successful gateway test provides evidence that:

* The local interface is operational
* The host can communicate with the gateway
* The local network connection is functioning sufficiently for the test
* The immediate next hop is reachable

However, it does **not** prove that:

* Every remote router is reachable
* The remote network is reachable
* The final destination is online
* The destination will accept the traffic
* A return route exists

Therefore:

> **Local gateway reachability does not prove end-to-end connectivity.**



# 10. Test 2 — Path Discovery

The path toward the remote destination was examined using:

```bash
traceroute [REMOTE_DESTINATION]
```

### Use

Attempts to reveal the sequence of network hops between the local host and the destination.

Conceptually:

```text
Mac
 ↓
Gateway
 ↓
Router
 ↓
Router
 ↓
Router
 ↓
Remote Network
 ↓
Destination
```

Several intermediate hops responded during the test.



# 11. Interpretation of Intermediate Hops

The traceroute results demonstrated that traffic was able to progress beyond the local gateway.

Conceptually:

```text
Mac
 ↓
Gateway             ✅
 ↓
Intermediate hop    ✅
 ↓
Intermediate hop    ✅
 ↓
Intermediate hop    ✅
 ↓
Destination         ❌
```

This shifted the troubleshooting focus away from the immediate local connection and toward the network beyond the gateway.



# 12. Important Distinction — Hop Response vs Destination Response

One of the most important lessons from this lab was:

> **A response from intermediate routers does not prove that the final destination is reachable.**

For example:

```text
Host → R1 → R2 → R3 → Destination
         ✅    ✅    ✅       ❌
```

The intermediate routers may respond while the destination does not.

Possible reasons include:

* Destination host is offline
* Firewall filtering
* ACL filtering
* ICMP filtering
* Missing return route
* Routing problem beyond the observed hops
* Other network-policy restrictions

Therefore, traceroute must be interpreted carefully.


# 13. Test 3 — Final Destination Reachability

The final destination was tested using:

```bash
ping -c 4 [REMOTE_DESTINATION]
```

### Result

The destination did not respond successfully.

Conceptually:

```text
Mac → Gateway → Several Hops → Destination
       ✅          ✅             ❌
```

This demonstrated that successful intermediate communication does not guarantee successful end-to-end communication.


# 14. Failure Localization

The combined evidence was:

```text
Gateway reachability       → SUCCESS
Route exists               → YES
Intermediate hops          → RESPONDING
Final destination          → NO RESPONSE
```

Therefore, the problem could reasonably be localized to:

```text
Beyond the local host
        ↓
Beyond the immediate gateway
        ↓
Somewhere along the remote path
or at the destination
```

The evidence did **not** justify claiming that one specific device was definitely responsible.



# 15. Troubleshooting Decision

Several possible causes were considered.

### A. Destination unavailable

The destination host may be offline or otherwise unreachable.

### B. Firewall or ACL filtering

A firewall or network ACL may be preventing the traffic or ICMP responses.

### C. Missing return route

The destination network may receive traffic but lack a route back toward the originating host.

### D. Other remote routing problem

A router farther along the path may have an incorrect or missing route.

Therefore, the correct professional conclusion was:

> **Additional investigation is required to determine the exact root cause.**



# 16. Evidence-Based Troubleshooting

The troubleshooting process followed this sequence:

```text
1. Check local route
        ↓
2. Identify next hop
        ↓
3. Test next-hop reachability
        ↓
4. Trace path
        ↓
5. Test final destination
        ↓
6. Compare results
        ↓
7. Localize the problem
        ↓
8. Investigate possible remote causes
```

This approach prevents premature conclusions.



# 17. Troubleshooting Commands

### Inspect routing table

```bash
netstat -rn -f inet
```

### Determine selected route

```bash
route -n get [DESTINATION]
```

### Test gateway

```bash
ping -c 4 [GATEWAY]
```

### Trace path

```bash
traceroute [DESTINATION]
```

### Test final destination

```bash
ping -c 4 [DESTINATION]
```

Each command provides a different type of evidence.


# 18. What Each Tool Tells Us

| Tool                  | Main Question                                     |
| --------------------- | ------------------------------------------------- |
| `netstat -rn -f inet` | What routes exist?                                |
| `route -n get`        | Which route will be selected?                     |
| `ping` gateway        | Can I reach my next hop?                          |
| `traceroute`          | What path appears between me and the destination? |
| `ping` destination    | Does the destination respond to this test?        |

Together, these tools provide a basic host-level routing troubleshooting toolkit.



# 19. Important Troubleshooting Lesson

The lab demonstrated the difference between:

```text
Reachability
```

and:

```text
Routing correctness
```

A route can exist without the destination being reachable.

Likewise:

```text
Gateway reachable
```

does not automatically mean:

```text
Destination reachable
```

A successful route selection only tells us what forwarding decision the host intends to make.

It does not guarantee that every device along the path will successfully forward the packet.



# 20. Root-Cause Reasoning

Based on the available evidence, the local host and immediate gateway were less likely to be the primary cause because:

```text
Local interface        → functioning
Gateway reachability   → successful
Route selection        → valid
Several hops            → responding
Final destination       → not responding
```

The investigation therefore moved toward:

```text
Remote path
     OR
Remote network
     OR
Destination host
```

This is an example of **failure localization**.



# 21. Security Considerations

The same troubleshooting techniques are relevant to cybersecurity.

Understanding the network path helps security professionals investigate:

* Network segmentation
* Firewall behavior
* ACLs
* Traffic filtering
* Network boundaries
* Unexpected traffic paths
* Remote access problems
* Routing-based security issues

However, tools such as `ping` and `traceroute` do not reveal the complete security state of a network.

A device may intentionally suppress diagnostic traffic as a security measure.



# 22. Lessons Learned

### 1. The next hop is determined by the selected route

```text
Destination
     ↓
Route selection
     ↓
Next hop
     ↓
Interface
```

### 2. Gateway reachability is only a local checkpoint

A reachable gateway proves that the host can reach its immediate next hop.

### 3. Traceroute reveals path information

It can show intermediate responding devices, but it is not a perfect representation of every packet's actual path.

### 4. Intermediate responses do not prove destination reachability

A destination can remain unreachable even when several routers respond.

### 5. Troubleshooting should be evidence-driven

Each test should narrow the possible failure location.

### 6. Do not confuse localization with root-cause identification

We can determine:

```text
Problem is likely beyond the local gateway
```

without yet knowing:

```text
Exactly which device or configuration caused it
```



# 23. Practical Skills Demonstrated

After completing this lab, I can:

* Identify a route's next hop
* Identify the outgoing interface
* Verify route selection
* Test gateway reachability
* Trace a network path
* Test final destination reachability
* Compare intermediate and destination responses
* Localize a routing/connectivity problem
* Develop possible failure hypotheses
* Distinguish evidence from assumptions
* Use multiple diagnostic tools together
* Follow a structured troubleshooting workflow



# 24. Foundation-to-Advanced Connection

The troubleshooting process established here forms the foundation for more advanced network diagnostics:

```text
Routing Tables
       ↓
Route Selection
       ↓
Next-Hop Analysis
       ↓
Path Discovery
       ↓
Reachability Testing
       ↓
Failure Localization
       ↓
Packet Analysis
       ↓
Firewall / ACL Troubleshooting
       ↓
Dynamic Routing Troubleshooting
       ↓
Advanced Network Operations
```



# 25. Connection to Cybersecurity

Network troubleshooting is closely connected to security analysis.

A security professional needs to understand:

```text
Where traffic originates
        ↓
Where it travels
        ↓
Which routers handle it
        ↓
Where filtering occurs
        ↓
Where communication stops
```

This knowledge becomes important when analyzing:

* Firewalls
* Network segmentation
* Access-control policies
* Remote-access systems
* Security monitoring
* Network attacks
* Cloud security



# 26. Final Practical Workflow

The complete troubleshooting workflow demonstrated in this lab was:

```text
Destination
     ↓
Check routing table
     ↓
Determine selected route
     ↓
Identify next hop
     ↓
Test next hop
     ↓
Trace path
     ↓
Test destination
     ↓
Compare evidence
     ↓
Localize failure
     ↓
Investigate possible causes
```



# 27. Lab Evidence Summary

The practical investigation produced the following evidence:

```text
Local interface
      ↓
      ✅

Gateway
      ↓
      ✅

Route selection
      ↓
      ✅

Several intermediate hops
      ↓
      ✅

Final destination response
      ↓
      ❌
```

The evidence therefore indicated that the connectivity problem was **not immediately explained by a failure of the local interface or immediate gateway**.

Further investigation would be required to determine whether the issue involved the remote network, filtering, routing, or the destination itself.



# 28. Conclusion

This lab combined route analysis with practical connectivity troubleshooting.

The investigation demonstrated that understanding a routing table is only the beginning of troubleshooting.

A network administrator must also determine:

```text
What route was selected?
        ↓
Who is the next hop?
        ↓
Can the next hop be reached?
        ↓
What path does the traffic appear to take?
        ↓
Does the final destination respond?
        ↓
Where can the failure reasonably be localized?
```

The most important lesson from this lab was:

> **Intermediate network reachability does not prove end-to-end reachability.**

The evidence gathered from routing tables, `route -n get`, `ping`, and `traceroute` provides a structured foundation for diagnosing more complex network failures.


**Core skills demonstrated:** Next-hop reasoning, path analysis, reachability testing, failure localization, and evidence-based network troubleshooting.
