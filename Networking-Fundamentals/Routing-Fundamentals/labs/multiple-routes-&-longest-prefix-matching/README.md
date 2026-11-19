# Lab 6 — Multiple Routes & Longest-Prefix Matching

## 1. Overview

This lab focused on understanding how a host selects a route when **multiple routing-table entries match the same destination**.

The lab built on the static-routing concepts established in Lab 5 and introduced a practical demonstration of **longest-prefix matching**.

A broad static route was configured for:

```text
10.20.0.0/16
```

A more-specific route was then configured for:

```text
10.20.30.0/24
```

The routing behavior was tested against multiple destinations to observe which route macOS selected.

The lab was performed using the host's actual IPv4 routing table rather than a simulated environment.


# 2. Scenario — Problem Being Solved

A host has multiple routes that may potentially match a destination.

The problem being investigated was:

> When more than one route matches a destination, how does the host decide which route to use?

The lab therefore demonstrated:

* Multiple matching routes
* `/16` versus `/24` prefixes
* Longest-prefix matching
* Specific route selection
* Default-route fallback
* Route verification
* Comparison of different destinations

---

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
                   │ Next-Hop /    │
                   │ Gateway       │
                   └───────┬───────┘
                           │
                  ┌────────┴────────┐
                  │                 │
             10.20.30.0/24     Other 10.20.x.x
                  │                 │
                  ▼                 ▼
             10.20.30.50       10.20.40.50

```

Two overlapping routing instructions were deliberately created:

```text
10.20.0.0/16
10.20.30.0/24
```

The purpose was to observe which one would be selected for different destinations.

The actual environment-specific gateway and host information have been masked.

---

# 4. Objectives

By completing this lab, I aimed to learn how to:

* Understand overlapping routes
* Understand route prefixes
* Compare `/16` and `/24` networks
* Apply longest-prefix matching
* Add multiple static routes
* Determine which routes match a destination
* Determine which route wins when multiple routes match
* Verify route selection using `route -n get`
* Understand the relationship between specific routes and the default route
* Test different destinations against the same routing table
* Understand how route selection changes when a more-specific route is removed

---

# 5. Environment

| Item                        | Details               |
| --------------------------- | --------------------- |
| Device                      | Mac                   |
| Operating System            | macOS                 |
| Network Interface           | `en0`                 |
| Connection                  | Wi-Fi                 |
| Addressing                  | IPv4                  |
| Routing-table command       | `netstat -rn -f inet` |
| Route inspection command    | `route -n get`        |
| Route configuration command | `route -n add`        |

Environment-specific IP addresses and MAC addresses have been masked where appropriate.

---

# 6. Important Concepts

## 6.1 Route Prefix

A routing prefix identifies the range of destination addresses covered by a route.

For example:

```text
10.20.0.0/16
```

covers a much larger range than:

```text
10.20.30.0/24
```

Conceptually:

```text
10.20.0.0/16
└── 10.20.x.x

10.20.30.0/24
└── 10.20.30.x
```

Therefore:

```text
10.20.30.0/24
```

is more specific than:

```text
10.20.0.0/16
```

---

# 7. Longest-Prefix Matching

When multiple routes match a destination, the routing system selects the route with the **longest prefix**.

For example:

```text
Destination:
10.20.30.50

Matching routes:

10.20.0.0/16       ✓
10.20.30.0/24      ✓

Selected route:

10.20.30.0/24
```

The `/24` route wins because it provides a more specific match.

The general principle is:

```text
More specific
     ↓
/32
/24
/16
/8
/0
     ↓
Less specific
```

---

# 8. Default Route

The host also had a default route:

```text
default → [MASKED_GATEWAY]
```

The default route represents:

```text
0.0.0.0/0
```

It matches any IPv4 destination for which a more-specific route does not exist.

Therefore, route selection can be visualized as:

```text
Specific route exists?
       │
   ┌───┴───┐
  YES      NO
   ↓        ↓
Use most   Use default
specific   route
route
```

---

# 9. Initial Routing State

Before adding the experimental routes, the host had a default route.

Conceptually:

```text
default → [MASKED_GATEWAY] → en0
```

A specific route for:

```text
10.20.0.0/16
```

was not initially present.

A specific route for:

```text
10.20.30.0/24
```

was also not initially present.

---

# 10. Command — Inspect the Routing Table

```bash
netstat -rn -f inet
```

### Use

Displays the host's IPv4 routing table.

It was used throughout the lab to verify:

* Existing routes
* Newly added routes
* Default route
* Gateway
* Interface
* Route removal

---

# 11. Command — Add the `/16` Route

The following command was used:

```bash
sudo route -n add -net 10.20.0.0/16 [MASKED_GATEWAY]
```

### Use

Creates a static route covering the:

```text
10.20.0.0/16
```

network.

The resulting routing instruction was conceptually:

```text
10.20.0.0/16
       ↓
[MASKED_GATEWAY]
       ↓
en0
```

---

# 12. Verification — `/16` Route

The routing table was checked using:

```bash
netstat -rn -f inet
```

The table showed an entry equivalent to:

```text
10.20/16    [MASKED_GATEWAY]    UGSc    en0
```

This confirmed that the `/16` static route had been installed.

---

# 13. Command — Determine the Selected Route

The following command was used:

```bash
route -n get 10.20.30.50
```

### Use

Determines which routing-table entry macOS selects for the specified destination.

This command was particularly useful because it showed the **actual forwarding decision** made by the operating system.

---

# 14. `/16` Route Selection

With only the `/16` route installed:

```text
Destination:

10.20.30.50
```

matched:

```text
10.20.0.0/16
```

Therefore, the `/16` route was selected.

Conceptually:

```text
10.20.30.50
      ↓
10.20.0.0/16
      ↓
[MASKED_GATEWAY]
      ↓
en0
```

---

# 15. Command — Add the More-Specific `/24` Route

The following command was then used:

```bash
sudo route -n add -net 10.20.30.0/24 [MASKED_GATEWAY]
```

### Use

Creates a more-specific static route for:

```text
10.20.30.0/24
```

The routing table now contained two overlapping routes:

```text
10.20.0.0/16
10.20.30.0/24
```

---

# 16. Verification — Multiple Routes

The routing table was inspected again:

```bash
netstat -rn -f inet
```

The relevant entries were conceptually:

```text
10.20/16       [MASKED_GATEWAY]    UGSc    en0
10.20.30/24    [MASKED_GATEWAY]    UGSc    en0
```

This demonstrated that both routes existed simultaneously.

---

# 17. Test — Destination `10.20.30.50`

The route was inspected:

```bash
route -n get 10.20.30.50
```

### Matching routes

The destination matched both:

```text
10.20.0.0/16       ✓
10.20.30.0/24      ✓
```

The `/24` route was selected.

The result was conceptually:

```text
10.20.30.50
      ↓
10.20.30.0/24
      ↓
[MASKED_GATEWAY]
      ↓
en0
```

---

# 18. Why the `/24` Route Won

The two routes had different prefix lengths:

```text
10.20.0.0/16
10.20.30.0/24
```

The `/24` contains more network bits and therefore identifies a smaller, more specific network.

Therefore:

```text
/24 > /16
```

in terms of route specificity.

This is the practical demonstration of:

> **Longest-prefix matching.**

---

# 19. Test — Destination `10.20.40.50`

The following command was used:

```bash
route -n get 10.20.40.50
```

### Matching routes

```text
10.20.0.0/16       ✓
10.20.30.0/24      ✗
```

`10.20.40.50` belongs to the larger:

```text
10.20.0.0/16
```

range, but not to:

```text
10.20.30.0/24
```

Therefore, the `/16` route was selected.

Conceptually:

```text
10.20.40.50
      ↓
10.20.0.0/16
      ↓
[MASKED_GATEWAY]
      ↓
en0
```

---

# 20. Test — Destination `10.20.255.50`

The following command was used:

```bash
route -n get 10.20.255.50
```

The destination matched:

```text
10.20.0.0/16       ✓
10.20.30.0/24      ✗
```

Therefore, the `/16` route was selected.

This reinforced the fact that the `/24` route only covers:

```text
10.20.30.x
```

while the `/16` covers the wider:

```text
10.20.x.x
```

range.

---

# 21. Test — Destination `8.8.8.8`

The following command was used:

```bash
route -n get 8.8.8.8
```

Neither of the experimental routes matched:

```text
10.20.0.0/16       ✗
10.20.30.0/24      ✗
```

Therefore, the default route was selected.

Conceptually:

```text
8.8.8.8
   ↓
No specific 10.20.x.x route
   ↓
Default route
   ↓
[MASKED_GATEWAY]
   ↓
en0
```

---

# 22. Route Selection Comparison

The experiments produced the following results:

| Destination    | `/16` Match | `/24` Match | Selected Route  |
| -------------- | ----------: | ----------: | --------------- |
| `10.20.30.50`  |           ✓ |           ✓ | `10.20.30.0/24` |
| `10.20.40.50`  |           ✓ |           ✗ | `10.20.0.0/16`  |
| `10.20.255.50` |           ✓ |           ✗ | `10.20.0.0/16`  |
| `8.8.8.8`      |           ✗ |           ✗ | Default route   |

This table provides direct evidence of longest-prefix matching and default-route fallback.

---

# 23. Important Distinction — Destination Host vs Destination Network

The lab reinforced the distinction between a **destination host** and a **destination network**.

For example:

```text
Destination host:
10.20.30.50
```

belongs to:

```text
Destination network:
10.20.30.0/24
```

Therefore:

```text
10.20.30.0
```

is the network address, not the individual host being contacted.

The routing table uses the network prefix to determine which destinations a route covers.

---

# 24. Route Selection Logic

The practical route-selection process demonstrated in this lab can be represented as:

```text
Destination IP
      ↓
Compare against routing entries
      ↓
Find all matching routes
      ↓
Are there multiple matches?
      │
   ┌──┴──┐
  YES    NO
   ↓      ↓
Choose   Use the
longest  matching
prefix   route
   │
   ↓
Determine next hop
   ↓
Determine outgoing interface
```

If no specific route matches:

```text
Destination
     ↓
No specific match
     ↓
Default route /0
     ↓
Next hop
```

---

# 25. Deliberate Comparison with the Default Route

The default route:

```text
0.0.0.0/0
```

can technically match every IPv4 destination.

However, it loses whenever a more-specific matching route exists.

For:

```text
10.20.30.50
```

the system can conceptually see:

```text
0.0.0.0/0          ✓
10.20.0.0/16       ✓
10.20.30.0/24      ✓
```

The winner is:

```text
10.20.30.0/24
```

because it is the longest matching prefix.



# 26. Cleanup

The temporary experimental routes were removed after the lab:

```text
10.20.30.0/24
10.20.0.0/16
```

The routing table was then verified to ensure the temporary entries were no longer present.

This prevented the experimental routes from affecting subsequent networking tests.

---

# 27. Troubleshooting Perspective

The lab also demonstrated how route-selection problems can be investigated systematically.

When a destination behaves unexpectedly:

### Step 1 — Inspect the routing table

```bash
netstat -rn -f inet
```

### Step 2 — Ask the operating system which route it selected

```bash
route -n get <destination>
```

### Step 3 — Identify the matching prefix

Determine whether the destination belongs to:

```text
Specific network
```

or only:

```text
Default route
```

### Step 4 — Compare competing prefixes

For example:

```text
/16 vs /24
```

### Step 5 — Apply longest-prefix matching

The most specific matching route should be selected.

This provides a practical troubleshooting method rather than relying on assumptions.



# 28. Key Lessons Learned

### 1. Multiple routes can exist for overlapping address ranges

For example:

```text
10.20.0.0/16
10.20.30.0/24
```

can coexist in the same routing table.

### 2. The most specific route wins

```text
10.20.30.0/24
```

wins over:

```text
10.20.0.0/16
```

for destinations inside `10.20.30.0/24`.

### 3. A route prefix determines its scope

A `/24` covers a smaller range than a `/16`.

### 4. The default route is the least-specific route

```text
0.0.0.0/0
```

acts as the fallback when no more-specific route matches.

### 5. `route -n get` reveals the actual decision

It is useful for determining exactly which route macOS will use.

### 6. Destination hosts belong to destination networks

For example:

```text
10.20.30.50
```

is a host inside:

```text
10.20.30.0/24
```

### 7. Routing decisions are based on prefixes

The host does not simply choose a route because it appears first in the routing table.

It evaluates which route provides the best match.



# 29. Practical Skills Demonstrated

After completing this lab, I can:

* Read overlapping routing entries
* Explain prefix length
* Compare `/16`, `/24`, and `/0`
* Explain longest-prefix matching
* Add multiple static routes
* Determine which routes match a destination
* Predict which route will win
* Verify route selection using macOS
* Identify the destination network
* Distinguish a destination host from a network address
* Explain default-route fallback
* Use routing-table evidence during troubleshooting
* Remove temporary routing configuration safely



# 30. Foundation-to-Advanced Connection

The concept demonstrated here is fundamental to more advanced routing technologies.

```text
IPv4 Addressing
       ↓
Subnetting
       ↓
Routing Tables
       ↓
Longest-Prefix Matching
       ↓
Static Routing
       ↓
Dynamic Routing
       ↓
OSPF / BGP
       ↓
Network Engineering
       ↓
Cloud Routing
       ↓
Advanced Network Troubleshooting
```

Even complex routers ultimately need to determine:

> **Which route is the best match for this destination?**



# 31. Connection to Cybersecurity

Understanding route selection is important for cybersecurity because security professionals need to understand how traffic moves through a network.

Routing knowledge supports understanding of:

* Network segmentation
* Traffic paths
* Security boundaries
* Firewall placement
* Network monitoring
* Traffic analysis
* Attack paths
* Routing misconfigurations
* Cloud network security

The security-specific applications will be explored later in the cybersecurity portion of the learning path.

---

# 32. Final Practical Summary

The lab demonstrated the following:

```text
                    Destination
                         │
                         ▼
                 10.20.30.50
                         │
             ┌───────────┴───────────┐
             │                       │
        10.20.0.0/16          10.20.30.0/24
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                  /24 is more specific
                         │
                         ▼
                   Selected route
```

For another destination:

```text
10.20.40.50
      ↓
10.20.30.0/24 does not match
      ↓
10.20.0.0/16 matches
      ↓
/16 selected
```

For an unrelated destination:

```text
8.8.8.8
   ↓
No specific route matches
   ↓
Default route /0
   ↓
Selected
```



# 33. Conclusion

This lab provided a practical demonstration of **longest-prefix matching** using a real macOS routing table.

By configuring overlapping routes and testing different destinations, I demonstrated that routing decisions are based on the **most specific matching prefix**.

The key principle established was:

> **When multiple routes match a destination, the route with the longest prefix is selected.**

The lab also reinforced that:

```text
Destination host
        ≠
Destination network
        ≠
Route
        ≠
Next hop
```

These distinctions are essential for understanding routing and will be used directly in the final routing integration exercise.

### Result

**LAB 6 — COMPLETE ✅**

**Core skill demonstrated:** Ability to analyze multiple routing entries, apply longest-prefix matching, determine the selected route, and explain default-route fallback.
