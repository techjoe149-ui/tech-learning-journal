# Routing Fundamentals — Lab 2: Local vs Remote Traffic, Routing, ARP and Layer 2 Delivery

## 1. Scenario — Problem Being Solved

A host needs to communicate with another IPv4 destination, but the method of delivery depends on whether the destination is on the local network or on a remote network.

The problem investigated in this lab was:

> How does a host determine whether an IPv4 destination is local or remote, and how does that decision determine which MAC address is used for Ethernet delivery?

The lab used a real macOS network environment to observe the relationship between:

* IPv4 addressing
* Subnets
* Routing tables
* Default gateways
* ARP
* MAC addresses
* Ethernet interfaces
* Local and remote traffic



## 2. Objective

The objectives were to:

1. Determine whether an IPv4 destination is local or remote.
2. Understand how the subnet determines local versus remote delivery.
3. Identify the route selected for a destination.
4. Understand the role of the default gateway for remote destinations.
5. Identify which MAC address is required for local and remote delivery.
6. Relate Layer 3 routing decisions to Layer 2 Ethernet delivery.
7. Verify these concepts using real terminal commands and network traffic.
8. Practice troubleshooting when the network environment changes unexpectedly.



## 3. Architecture — Components Involved

The lab involved the following components:

```text
                    LOCAL NETWORK
              ┌───────────────────────┐
              │                       │
        MacBook                        │
    <LOCAL_HOST_IP>                   │
        en0                            │
              │                       │
              ├──── <LOCAL_DEVICE_IP> │
              │    MAC: XX:XX:XX:XX:XX:XX
              │                       │
              └──── <DEFAULT_GATEWAY> │
                   Default Gateway    │
                   MAC: XX:XX:XX:XX:XX:XX
              └───────────────────────┘
                         │
                         │
                      Internet
                         │
                      8.8.8.8
```

### Main components

* **Host:** MacBook running macOS
* **Network interface:** `en0`
* **IPv4 address:** `<LOCAL_HOST_IP>`
* **Local network:** `<LOCAL_NETWORK>/<PREFIX>`
* **Default gateway:** `<DEFAULT_GATEWAY>`
* **Gateway MAC:** `XX:XX:XX:XX:XX:XX`
* **Local test host:** `<LOCAL_DEVICE_IP>`
* **Local host MAC:** `XX:XX:XX:XX:XX:XX`
* **Remote test destination:** `8.8.8.8`

> **Privacy note:** Actual private IP addresses and MAC addresses observed during the lab have been masked because the README is intended for a public portfolio.



# 4. Environment

### Device

* macOS laptop
* Wi-Fi connection
* Interface: `en0`

### Commands used

```bash
ipconfig getifaddr en0
route -n get default
route -n get 8.8.8.8
netstat -rn -f inet
arp -a
ping -c 1 <destination>
sudo tcpdump -i en0 -e -n arp
sudo arp -d <IP>
```


# 5. Implementation

## 5.1 Identify the Host IP Address

Command:

```bash
ipconfig getifaddr en0
```

The command returned the host's active IPv4 address.

The actual address has been masked in this public documentation:

```text
<LOCAL_HOST_IP>
```

This established the IP address currently assigned to the `en0` interface.

---

## 5.2 Identify the Default Gateway

Command:

```bash
route -n get default
```

The command initially returned a default gateway associated with `en0`.

For the public version of this documentation:

```text
gateway: <DEFAULT_GATEWAY>
interface: en0
```

This established that traffic without a more specific route would be sent toward the default gateway.



## 5.3 Inspect the ARP Table

Command:

```bash
arp -a
```

The ARP table contained IP-to-MAC mappings for locally reachable devices.

Example sanitized representation:

```text
<LOCAL_DEVICE_IP> → XX:XX:XX:XX:XX:XX
<OTHER_LOCAL_IP> → XX:XX:XX:XX:XX:XX
<DEFAULT_GATEWAY> → XX:XX:XX:XX:XX:XX
```

This demonstrated the relationship:

```text
IPv4 address → MAC address
```

for locally reachable devices known to the host.

---

# 6. Local-Destination Experiment

A local destination was selected from the same subnet as the host.

```text
<LOCAL_DEVICE_IP>
```

The host determined that the address was local because it belonged to the same subnet.

The fundamental decision was:

```text
Host IP
    │
    │ same subnet
    ↓
Local destination
    │
    ↓
Direct Layer 2 delivery
```

The ARP table provided the corresponding MAC address:

```text
<LOCAL_DEVICE_IP> → XX:XX:XX:XX:XX:XX
```

### Connectivity test

```bash
ping -c 1 <LOCAL_DEVICE_IP>
```

The ping succeeded with:

```text
1 packets transmitted, 1 packets received
0.0% packet loss
```

### Interpretation

The destination was reachable directly on the local network.

The Ethernet destination MAC therefore corresponded to the destination device:

```text
Destination IP:
<LOCAL_DEVICE_IP>

Destination MAC:
XX:XX:XX:XX:XX:XX

Interface:
en0
```



# 7. Remote-Destination Experiment

A remote destination was selected:

```text
8.8.8.8
```

The destination was outside the local network.

The forwarding process was:

```text
Host
  │
  │ destination is remote
  ↓
Default Gateway
  │
  ↓
Internet
  │
  ↓
8.8.8.8
```

The host therefore needed to use the default gateway as the next local hop.

### Connectivity test

```bash
ping -c 1 8.8.8.8
```

Result:

```text
1 packets transmitted, 1 packets received
0.0% packet loss
```

The gateway's ARP mapping was represented as:

```text
<DEFAULT_GATEWAY> → XX:XX:XX:XX:XX:XX
```

Therefore, for the first Ethernet hop:

```text
Destination IP:
8.8.8.8

Next-hop IP:
<DEFAULT_GATEWAY>

Next-hop MAC:
XX:XX:XX:XX:XX:XX
```

The IP packet remained destined for `8.8.8.8`, while the Ethernet frame was initially addressed to the local gateway.



# 8. Routing Table Verification

Command:

```bash
route -n get 8.8.8.8
```

The command identified the gateway selected for the remote destination:

```text
gateway: <DEFAULT_GATEWAY>
interface: en0
```

The routing table was then inspected:

```bash
netstat -rn -f inet
```

Relevant entries were represented as:

```text
default            <DEFAULT_GATEWAY>      UGScg     en0
<LOCAL_NETWORK>    link#4                 UCS       en0
<DEFAULT_GATEWAY>  XX:XX:XX:XX:XX:XX      UHLWIir   en0
<LOCAL_DEVICE_IP>  XX:XX:XX:XX:XX:XX      UHLWI     en0
<LOCAL_HOST_IP>    link#4                 UCS       en0
```

This confirmed the relationship:

```text
8.8.8.8
   ↓
default route
   ↓
<DEFAULT_GATEWAY>
   ↓
en0
```



# 9. Verification — Evidence That It Worked

Several forms of evidence were collected.

## 9.1 Local connectivity

```bash
ping -c 1 <LOCAL_DEVICE_IP>
```

Result:

```text
1 packets transmitted, 1 packets received
0.0% packet loss
```

This verified successful communication with a local host.

## 9.2 Remote connectivity

```bash
ping -c 1 8.8.8.8
```

Result:

```text
1 packets transmitted, 1 packets received
0.0% packet loss
```

This verified successful communication with a remote destination.

## 9.3 ARP verification

```bash
arp -a | grep <LOCAL_DEVICE_IP>
```

The command confirmed an IP-to-MAC mapping:

```text
<LOCAL_DEVICE_IP> → XX:XX:XX:XX:XX:XX
```

The gateway mapping was also verified:

```text
<DEFAULT_GATEWAY> → XX:XX:XX:XX:XX:XX
```

## 9.4 Routing verification

```bash
route -n get 8.8.8.8
```

confirmed:

```text
gateway: <DEFAULT_GATEWAY>
interface: en0
```



# 10. Failure / Unexpected Behavior

Several unexpected behaviors occurred during the lab.

## 10.1 Incorrect command

The following command was entered:

```bash
ping -a | grep <IP_ADDRESS>
```

macOS returned the `ping` usage information because the destination host was missing.

The correct approach for filtering the ARP table was:

```bash
arp -a | grep <IP_ADDRESS>
```

### Lesson from failure

Terminal commands must be interpreted carefully. Similar-looking commands can perform completely different functions.



## 10.2 ARP entry could not be deleted

The command:

```bash
sudo arp -d <IP_ADDRESS>
```

returned:

```text
delete: cannot locate <IP_ADDRESS>
```

A subsequent ARP lookup produced no matching entry.

This demonstrated that an ARP entry cannot simply be deleted if it is not currently present in the ARP cache.



## 10.3 Unexpected ARP traffic

`tcpdump` captured ARP traffic generated by other devices visible on the network.

The public version of the capture is intentionally sanitized:

```text
XX:XX:XX:XX:XX:XX > ff:ff:ff:ff:ff:ff
Request who-has <IP_ADDRESS>

XX:XX:XX:XX:XX:XX > XX:XX:XX:XX:XX:XX
Reply <IP_ADDRESS> is-at XX:XX:XX:XX:XX:XX
```

This demonstrated that `tcpdump` can observe traffic occurring on the connected network rather than only traffic generated by the local machine.



# 11. Troubleshooting

## Evidence collected

The following commands were used:

```bash
ipconfig getifaddr en0
route -n get default
route -n get 8.8.8.8
netstat -rn -f inet
arp -a
ping -c 1 <destination>
sudo tcpdump -i en0 -e -n arp
```

These provided evidence about:

* Current IP configuration
* Default gateway
* Destination-specific routing
* ARP mappings
* Connectivity
* Layer 2 ARP traffic



# 12. Root Cause

The major unexpected issue was that the Mac's network environment changed during the lab.

Earlier in the lab, the host was using a different private network and gateway.

Later, the routing table showed that the host had moved to another private network.

This meant that previously collected IP, gateway and ARP information could no longer automatically be treated as the current network state.

The root troubleshooting principle was:

> Network configuration must be inspected at the time of troubleshooting rather than assumed from earlier observations.



# 13. Resolution

The network state was re-established using:

```bash
ipconfig getifaddr en0
netstat -rn -f inet
route -n get 8.8.8.8
arp -a
```

The current routing and ARP information was then used for the remainder of the lab.

This allowed the local-versus-remote experiments to remain accurate despite the network change.


# 14. Security Considerations

ARP does not provide strong authentication, which creates opportunities for attacks on local networks.

Potential risks include:

* ARP spoofing
* ARP cache poisoning
* Traffic interception
* Man-in-the-middle attacks
* Incorrect IP-to-MAC mappings

At foundation level, the important security lesson is:

> Understanding normal ARP behavior is necessary before understanding how ARP-based attacks and defenses work.

Actual device MAC addresses observed during the lab have deliberately been removed from this public documentation.


# 15. Automation Opportunities

Several parts of this investigation could eventually be automated.

A future script could collect:

```text
Current IP
     ↓
Subnet
     ↓
Default gateway
     ↓
Routing table
     ↓
ARP/neighbor mappings
     ↓
Connectivity tests
```

A future Python or shell-based troubleshooting tool could produce a report such as:

```text
Destination: 8.8.8.8
Classification: Remote
Next hop: <DEFAULT_GATEWAY>
Interface: en0
Gateway MAC: <GATEWAY_MAC>
Connectivity: Reachable
```

This connects the networking foundation to future Python, Linux and network-automation skills.

---

# 16. Specific Skills Learned

### Networking skills

* Identifying local versus remote IPv4 destinations
* Reading subnet boundaries
* Understanding `/22` and `/24` networks
* Reading routing tables
* Identifying default gateways
* Understanding next-hop forwarding
* Reading ARP tables
* Mapping IPv4 addresses to MAC addresses
* Understanding local Ethernet delivery
* Understanding remote Ethernet delivery
* Using `ping` for connectivity verification
* Using `tcpdump` to observe ARP traffic

### Troubleshooting skills

* Establishing the current network state
* Comparing expected and actual routing information
* Investigating unexpected command output
* Distinguishing local traffic from traffic generated by another host
* Collecting evidence before forming a conclusion
* Recognizing when previously collected information has become stale

---

# 17. Integration With Previously Learned Foundations

This lab builds directly on earlier networking fundamentals.

## IP addressing

Previously learned:

```text
IP address + subnet mask
```

This lab applied that knowledge to determine whether destinations were local or remote.

## Ethernet and MAC addressing

Previously learned:

```text
IP → MAC → Ethernet frame
```

This lab showed when the destination MAC is the actual destination and when it is the gateway.

## ARP

Previously learned:

```text
IPv4 address → MAC address
```

This lab demonstrated why that mapping matters for actual packet delivery.

## Switching

Previously learned:

```text
MAC address → switch port
```

This lab provided the Layer 3 decision that occurs before the Layer 2 switching process:

```text
Destination IP
      ↓
Routing decision
      ↓
Next-hop IP
      ↓
ARP / MAC resolution
      ↓
Ethernet frame
      ↓
Switch forwarding
```

---

# 18. Connection to Future Intermediate and Advanced Skills

### Intermediate networking

These concepts will support:

* Static routing
* Default routing
* Dynamic routing
* VLANs
* Inter-VLAN routing
* Network segmentation
* Routing between multiple networks
* More advanced troubleshooting

### Advanced networking

The same concepts eventually support:

* OSPF and other routing protocols
* Enterprise network design
* ACLs
* Firewalls
* VPNs
* Network monitoring
* Packet analysis
* Network automation

### Cybersecurity

Understanding:

```text
IP
↓
Routing
↓
ARP
↓
MAC
↓
Ethernet
```

is essential for understanding:

* ARP spoofing
* Man-in-the-middle attacks
* Packet interception
* Network reconnaissance
* Traffic analysis
* Network-based security controls

### Automation

The information collected manually in this lab can eventually be collected and analyzed automatically using:

* Shell scripting
* Python
* Network automation tools
* Monitoring systems
* APIs

---

# 19. Lessons Learned

The most important lesson was that **routing and Layer 2 networking are connected processes**.

A host first determines where an IP packet needs to go. It then determines the appropriate local next hop and obtains the MAC address required to deliver the Ethernet frame.

### Local destination

```text
Destination IP
      ↓
Local?
      ↓
YES
      ↓
Destination MAC
      ↓
Direct Ethernet delivery
```

### Remote destination

```text
Destination IP
      ↓
Local?
      ↓
NO
      ↓
Default gateway / next hop
      ↓
Gateway MAC
      ↓
Ethernet delivery to gateway
```

Another important lesson was that **the IP destination and Ethernet destination are not always the same device**.

For example:

```text
IP destination:
8.8.8.8

Ethernet destination for first hop:
<DEFAULT_GATEWAY>
MAC: <GATEWAY_MAC>
```

The lab also reinforced a practical troubleshooting principle:

> **Always verify the current network state before reasoning about what the network should be doing.**

The network changed during the lab, and inspecting the routing table revealed that change.


# 20. Final Conclusion

This lab demonstrated how a host connects Layer 3 routing decisions with Layer 2 Ethernet delivery.

The practical workflow established was:

```text
Destination IP
      ↓
Determine local or remote
      ↓
Select route
      ↓
Determine next hop
      ↓
Resolve required MAC address
      ↓
Build Ethernet frame
      ↓
Transmit through network interface
```

The lab therefore connected the foundational concepts of:

**IP addressing → subnetting → routing → ARP → MAC addressing → Ethernet delivery → troubleshooting**

This provides the foundation required for progressing through the remaining routing fundamentals and eventually into intermediate networking, network security and automation.



## Public Portfolio Privacy

Actual IP addresses, MAC addresses and other network identifiers collected during the live lab have been masked in this README.

The original terminal outputs should be retained privately as supporting evidence but should not be committed to a public repository without sanitization.
