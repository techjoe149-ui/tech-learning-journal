
1. Ethernet

Ethernet is a fundamental networking technology used to communicate devices across a local network.

At the foundation level, Ethernet is primarily concerned with:

Layer 2 communication
Ethernet frames
MAC addresses
Local delivery of frames
Communication between devices connected through Ethernet networks

2. Ethernet Frame

An Ethernet frame is the Layer 2 data unit used to carry information across an Ethernet network.

At the  foundation level, the most important fields are:

Source MAC
Destination MAC
Payload

Example:

Source MAC:      AA:AA:AA:AA:AA:AA
Destination MAC: BB:BB:BB:BB:BB:BB

The:

Source MAC identifies the device sending the frame.

The:

Destination MAC identifies the intended Layer 2 recipient.

3. MAC Addresses

A MAC address is a Layer 2 hardware/network-interface address used for local network communication.

Example:

f0:18:98:56:cf:d2

My Mac's active Wi-Fi interface, en0, showed:

MAC: f0:18:98:56:cf:d2
IPv4: 192.168.100.21
Important distinction

A MAC address and IP address serve different purposes.

MAC → local Layer 2 delivery


IP → Layer 3 addressing between networks


4. Unicast, Broadcast & Multicast
Unicast

One sender → one intended receiver.

A ─────────→ B

Example:

Source MAC → Destination MAC
Broadcast

One sender → all relevant devices in the local broadcast domain.

The Ethernet broadcast MAC is:

ff:ff:ff:ff:ff:ff

My ARP experiment demonstrated this.

Multicast

One sender → a defined group of receivers.

At foundation level, I only need to recognize that multicast is different from both unicast and broadcast.



5. ARP

ARP = Address Resolution Protocol.

Its fundamental purpose is:

To discover the MAC address associated with an IPv4 address on the local network.

For example,my Mac needed to communicate with:

192.168.100.1

It could ask:

Who has 192.168.100.1?

The ARP request is broadcast:

Destination MAC:
ff:ff:ff:ff:ff:ff

The device owning that IP responds.

my capture showed:

Request:
Who-has 192.168.100.1
tell 192.168.100.21

followed by:

Reply:
192.168.100.1 is-at
2c:0b:ab:83:ac:31

Therefore:

192.168.100.1
       ↓
2c:0b:ab:83:ac:31
6. ARP Cache

Once a device learns an IP-to-MAC relationship, it can temporarily store it in its ARP cache.

I inspected mine using:

arp -a

then I observed:

192.168.100.1 → 2c:0b:ab:83:ac:31

I also encountered:

169.254.169.254 → incomplete

incomplete means the system has not successfully obtained a MAC address for that IPv4 address through ARP.

Key distinction
ARP cache:


IPv4 address → MAC address



7. Switches

A switch is a Layer 2 device that forwards Ethernet frames using MAC addresses.

Conceptually:

Device A ──┐
Device B ──┤
Device C ──┤── SWITCH
Device D ──┘

The switch maintains a:

MAC address table / CAM table



8. MAC/CAM Table

The switch's table maps:

MAC address → switch port

Example:

AA:AA:AA:AA:AA:AA → Port 1
BB:BB:BB:BB:BB:BB → Port 2
CC:CC:CC:CC:CC:CC → Port 3

This allows the switch to determine where to send frames.



9. MAC Learning

A switch learns from the source MAC address of an incoming frame.

Example:

Frame arrives on Port 3


Source MAC:
AA:AA:AA:AA:AA:AA

The switch learns:

AA:AA:AA:AA:AA:AA → Port 3
Critical rule

Source MAC → Learn

Destination MAC → Look up

The switch does not learn the destination's location from the source MAC.


10. Forwarding

If the destination MAC is known:

BB:BB:BB:BB:BB:BB → Port 5

the switch forwards the frame to Port 5.

Port 2
  ↓
SWITCH
  ↓
Port 5

Therefore:

Known destination → Forward

11. Flooding

If the destination MAC is unknown:

DD:DD:DD:DD:DD:DD

and there is no entry in the MAC table, the switch doesn't know which port leads to the destination.

It therefore floods the frame through the relevant other ports.

Also:

Broadcast frames are flooded.

Important distinction:

Unknown unicast flooding is not the same thing as an ARP broadcast.

12. Filtering

If the switch knows that the destination is reachable through the same port the frame arrived on, it does not send the frame back through that port.

This is filtering.

Foundation rule:

Destination on incoming port
          ↓
       FILTER
13. The Three Switching Behaviors

The fundamental decision process is:

             Frame arrives
                  ↓
          Learn source MAC
                  ↓
        Look up destination MAC
                  ↓
        ┌─────────┼─────────┐
        ↓         ↓         ↓
      Known     Unknown   Incoming
      other               port
        ↓         ↓         ↓
     FORWARD     FLOOD    FILTER

This is one of the most important pieces of your Phase 3 foundation.

14. Physical Ethernet

Ethernet communication can use physical media such as:

Copper

Uses electrical signals through twisted-pair copper cable.

Fiber

Uses light through optical fiber.

A physical connection can therefore be represented conceptually as:

Device ───── physical medium ───── Device


15. Network Interface vs Cable

These should not be confused.

Network interface

The device's network connection/interface.

Example from your Mac:

en0 → Wi-Fi
Ethernet cable

The physical medium carrying signals between Ethernet-capable devices.

Therefore:

Interface ≠ cable


16. Link Status

A network interface can have a physical/link state such as:

UP
DOWN

If the link is down, physical/link troubleshooting should happen before investigating higher-level problems such as:

IP addressing
DNS
Applications

Basic troubleshooting order:

Physical / Link
       ↓
IP
       ↓
Transport
       ↓
Application


17. Ethernet Frame vs Physical Signal

These are not the same thing.

Ethernet frame
      ↓
     bits
      ↓
physical representation
      ↓
physical medium

The Ethernet frame is the Layer 2 data structure.

The physical signal is how those bits are physically represented and carried across the medium.

🔑 Essential Relationships:

ARP CACHE
IPv4 → MAC
SWITCH MAC/CAM TABLE
MAC → PORT
ROUTING TABLE
Destination network → Next hop/interface
