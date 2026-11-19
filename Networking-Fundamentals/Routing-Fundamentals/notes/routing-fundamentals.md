# Routing Fundamentals

## Overview

Routing is the process of determining where network traffic should be sent so that it can reach its destination.

At the foundation level, routing answers:

> Where is the destination, and where should I send the packet next?

Routing operates primarily at **Layer 3 — the Network Layer** of the OSI model.


# 1. What Is Routing?

A device uses routing information to determine how to reach a destination IP network.

A simplified process is:

```text
Destination IP
      ↓
Routing table
      ↓
Find matching route
      ↓
Determine next hop/interface
      ↓
Forward packet


A router performs this process between different networks.


2. Router Function

A router connects different IP networks and forwards packets between them.

For example:

Network A
192.168.1.0/24
      |
      |
    Router
      |
      |
Network B
192.168.2.0/24

The router determines how traffic should move from one network to another.

3. Routing Table

A routing table contains information about reachable networks and how traffic should be forwarded.

A simplified routing table may look like:

Destination        Next Hop
192.168.1.0/24     directly connected
192.168.2.0/24     192.168.1.2
0.0.0.0/0          192.168.1.1

Important information can include:

Destination network
Gateway / next hop
Interface
Route type
Route status

On macOS, the routing table can be inspected using:

netstat -rn -f inet

4. Connected Routes

A connected route represents a network that is directly connected to an interface.

For example:

Interface:
10.101.141.170/22

Network:
10.101.140.0/22

The operating system knows that this network is directly reachable through the interface.

A directly connected destination does not need to be sent to the default gateway first.

5. Local vs Remote Destinations

Before sending traffic, the host determines whether the destination is:

Local/directly reachable
Remote/not directly reachable

Example:

Local network:
10.101.x.x/22

Destination:

10.101.142.xx

The destination belongs to the local network.

Therefore the host can communicate directly through the local network.

For a remote destination such as:

8.8.8.8

the host uses a route toward a router, normally the default gateway.

6. Default Route

A default route is the route used when no more-specific route matches the destination.

IPv4 default route:

0.0.0.0/0

For example:

0.0.0.0/0 → 10.101.143.254

This means:

If no more-specific route tells me where to send the packet, forward it toward 10.101.143.254.

The default gateway is therefore the next-hop router used by the default route.

7. Next Hop

The next hop is the immediate device/router to which traffic is forwarded on its way toward the final destination.

Example:

My Mac
10.101.141.170
      |
      ↓
10.101.143.254
      |
      ↓
Other routers
      |
      ↓
8.8.8.8

Here:

Final destination = 8.8.8.8
Next hop           = 10.101.143.254

The final destination and next hop are not necessarily the same device.

8. MAC Address vs Next-Hop IP

Routing and Ethernet work together.

For a remote destination:

Destination IP:
8.8.8.8

The host may determine:

Next hop:
10.101.143.254

It then needs the MAC address of the next hop in order to construct the Ethernet frame.

ARP can be used to discover the MAC address associated with the IPv4 next-hop address.

Example:

Gateway IP:
10.101.143.254

Gateway MAC:
c0:bc:9a:f5:e3:5f

Conceptually:

IP packet
Source IP → My IP
Destination IP → 8.8.8.8

Ethernet frame
Source MAC → My MAC
Destination MAC → Gateway MAC

The important distinction is:

The IP destination identifies where the packet ultimately needs to go, while the Ethernet destination MAC identifies the next device receiving the frame on the local link.

9. Static Routing

A static route is manually configured by an administrator.

Example:

192.168.20.0/24 → 192.168.10.2

This means:

To reach 192.168.20.0/24, forward traffic toward 192.168.10.2.

Static routes remain as configured until they are changed or removed.

10. Connected vs Static Routes
Connected route

Created because a network is directly connected to an active interface.

192.168.10.0/24
      ↓
directly connected
Static route

Manually configured:

192.168.20.0/24
      ↓
192.168.10.2

Therefore:

Connected → learned from directly connected interface
Static    → manually configured
11. Static Route vs Default Route

These terms describe different things.

Static

Describes how the route was configured.

Default

Describes the route's destination coverage.

A route can therefore be both:

Static + Default

For example:

0.0.0.0/0 → 10.101.143.254
12. Longest-Prefix Match

A router may have multiple routes that match a destination.

When multiple routes match:

The route with the longest prefix is preferred.

Example:

10.0.0.0/8
10.10.0.0/16
10.10.20.0/24

Destination:

10.10.20.50

All three routes can match.

The router chooses:

10.10.20.0/24

because:

/24 > /16 > /8

Therefore /24 is the most specific route.

13. Understanding a Route Match

A destination matches a route when the destination IP belongs to the network represented by that route.

Example:

10.101.140.0/22

This network covers:

10.101.140.x
10.101.141.x
10.101.142.x
10.101.143.x

Therefore:

10.101.142.77

matches the route.

But:

10.101.144.10

does not match.

The basic process is:

Destination IP
      ↓
Does it belong to this network?
      ↓
YES → route matches
NO  → route does not match
14. Routing Decision Process

At foundation level, the routing decision can be summarized as:

        Destination IP
              |
              ↓
        Routing table
              |
              ↓
      Find matching routes
              |
       ┌──────┴──────┐
       ↓             ↓
    One match    Multiple matches
       |             |
       |             ↓
       |       Longest prefix
       |             |
       └──────┬──────┘
              ↓
         Selected route
              ↓
        Next hop/interface
              ↓
          Forward packet

If no more-specific route exists:

Use default route
15. Foundation-Level Routing Troubleshooting

When troubleshooting connectivity, examine:

IP address
Subnet/prefix
Local vs remote destination
Routing table
Default route
Next hop
ARP resolution
Interface status
Packet behavior

Useful commands on macOS include:

ifconfig
ipconfig getifaddr en0
arp -a
route -n get default
netstat -rn -f inet
ping
traceroute

16.*Key Commands*

View interfaces
ifconfig

Get IPv4 address
ipconfig getifaddr en0

View ARP cache:
arp -a

View default route:
route -n get default

View IPv4 routing table:
netstat -rn -f inet

Test connectivity :
ping -c 4 <destination>

Trace a path:
traceroute <destination>


# 17. Key Foundation Distinctions

Destination vs next hop
Destination → where the packet ultimately needs to go
Next hop    → immediate device receiving the packet next

Connected vs static:

Connected → directly reachable network
Static    → manually configured route


Default route vs default gateway:

Default route   → routing-table rule
Default gateway → next-hop router used by that rule

IP vs MAC
IP  → Layer 3 addressing/routing
MAC → Layer 2 local-link delivery

