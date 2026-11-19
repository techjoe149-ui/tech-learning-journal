

# Lab 03 — Clearing and Rebuilding an ARP Entry

**File:** 

# Lab 03 — Clearing and Rebuilding an ARP Entry

## Objective

Remove an existing ARP cache entry and observe how ARP resolution occurs again when communication with the destination is required.

## Environment

- Operating System: macOS
- Active interface: `en0`
- Local IPv4: ``
- Gateway: 

## Step 1 — Inspect the Existing Entry

The ARP cache was inspected using:

arp -a

The gateway entry was:

192.168.100.1 → 2c:0b:ab:83:ac:31
Step 2 — Delete the ARP Entry

The following command was attempted:

arp -d <NETWORK-IP>

An initial attempt returned:

Operation not permitted

The operation was subsequently performed successfully with the required privileges.

The system confirmed:

192.168.100.1 (192.168.100.1) deleted
Step 3 — Trigger Communication

The gateway was contacted using:

ping -c 1<NETWORK IP>

The result was:

64 bytes from 192.168.100.1

with:

0.0% packet loss
Step 4 — Observe the Routing Information

The default route was inspected using:

route -n get default

The output showed:

gateway: 192.168.100.1
interface: en0

This confirmed that 192.168.100.1 was the default gateway for the system.

Troubleshooting

An incorrect ping command was initially entered:

ping -c 192.168.100.1

This resulted in:

invalid count of packets to transmit

The correct syntax was:

ping -c 1 192.168.100.


Result

Successfully removed the gateway's ARP entry, communicated with the gateway, and observed successful connectivity.

Lessons Learned

ARP cache entries can be removed and rebuilt.
Communication with a local IPv4 destination may require ARP resolution.
The default gateway is used for traffic destined outside the local network.
route -n get default can identify the default gateway and interface on macOS.