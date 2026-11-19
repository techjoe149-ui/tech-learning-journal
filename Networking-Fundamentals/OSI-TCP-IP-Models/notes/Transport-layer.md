# Transport Layer (Layer 4)

## 1. Introduction

The Transport Layer is Layer 4 of the OSI Model. It provides end-to-end communication between applications running on different devices.

The Network Layer uses IP addresses to identify and reach devices. The Transport Layer uses port numbers to identify the specific application or service that should receive the data.

For example, a laptop may simultaneously use a web browser, email, SSH, and a video-call application. They can share the same IP address while using different source and destination ports.

The Transport Layer primarily uses two protocols:

- TCP (Transmission Control Protocol)
- UDP (User Datagram Protocol)

TCP prioritizes reliability and ordered delivery. UDP prioritizes speed and low delay.

---

## 2. Transport Layer Position

```text
Layer 7 - Application
Layer 6 - Presentation
Layer 5 - Session
Layer 4 - Transport
Layer 3 - Network
Layer 2 - Data Link

3. Main Responsibilities
3.1 Segmentation

Large amounts of application data are divided into smaller units for transmission. for TCP, these units are commonly called segments . at the destination, the transport layer helps reconstruct the original data .

Application Identification

Port numbers identify the application or service associated with a connection.

Example:Destination IP:   192.168.1.10
Destination Port: 443

The IP address identifies the destination device.

The port identifies the service.

Therefore: IP address → Which device?
Port number → Which application/service?

Reliability

TCP can provide reliable communication through:

Sequence numbers
Acknowledgements
Retransmissions
Flow control
Congestion control

Multiplexing and Demultiplexing

A device can communicate with many applications simultaneously.

The Transport Layer allows data from multiple applications to share the same network connection and then directs incoming data to the appropriate application using port numbers.


Ports

A port is a logical number used by the operating system to identify a service or application.

An IP address alone is not enough to identify the application.

For example:

192.168.1.20:443

means:

Device: 192.168.1.20
Port:   443
Service: HTTPS
Source and Destination Ports

A TCP/UDP communication normally has both:

Source port
Destination port

Example:

Laptop                          Web Server

192.168.1.20:51542  -------->  142.250.x.x:443

Here:

192.168.1.20 is the client's IP address.
51542 is the client's temporary source port.
142.250.x.x is the server's IP address.
443 is the server's destination port.

The server can use the source IP and source port to identify which client connection the response belongs to.

This is why many devices can communicate with the same server simultaneously.

5. Common Port Numbers
Service	Protocol	Port
HTTP	TCP	80
HTTPS	TCP	443
SSH	TCP	22
DNS	UDP/TCP	53
DHCP Server	UDP	67
DHCP Client	UDP	68
FTP Data	TCP	20
FTP Control	TCP	21
SMTP	TCP	25
IMAP	TCP	143
IMAPS	TCP	993

Port numbers do not permanently belong to an application. They are conventions and can be changed by software configuration. However, many services use standardized well-known ports so that clients know where to connect.

6. TCP - Transmission Control Protocol

TCP is a connection-oriented and reliable transport protocol.

TCP is designed for situations where data must arrive correctly and in the correct order.

TCP provides:

Connection establishment
Reliable delivery
Ordered delivery
Error detection
Acknowledgements
Retransmission
Flow control
Congestion control
Connection termination

Examples of applications that commonly use TCP include:

HTTPS
HTTP
SSH
FTP
Many email protocols
Many database connections
7. TCP Three-Way Handshake

TCP establishes a connection using a three-way handshake.

Client                         Server

SYN  ----------------------->

     <------------------- SYN-ACK

ACK  ----------------------->
Step 1 - SYN

The client sends a SYN packet to request a TCP connection.

The client is essentially saying:

I want to establish a TCP connection.

Step 2 - SYN-ACK

The server responds with SYN-ACK.

The server is acknowledging the client's request and also providing its own synchronization information.

Step 3 - ACK

The client sends an ACK.

The connection is now established and application data can be exchanged.

The handshake establishes the state necessary for reliable TCP communication.

8. TCP Sequence Numbers

TCP uses sequence numbers to keep track of the position of data in a byte stream.

They allow the receiver to determine:

Which data has arrived.
Which data is missing.
The correct order of the data.

Example:

Sender:

Segment A
Segment B
Segment C
Segment D

If the network delivers them out of order:

A
C
B
D

TCP can use sequence information to reconstruct the correct data stream.

Important distinction:

IP is concerned with delivering packets between devices.

TCP is concerned with maintaining the correct application data stream.

9. TCP Acknowledgements

TCP uses acknowledgements to confirm successful receipt of data.

For example:

Sender → Segment 1
Receiver → ACK

The acknowledgement tells the sender that the receiver has successfully received the relevant data.

TCP uses this mechanism as part of its reliability system.

10. TCP Retransmission

If data is lost, TCP can retransmit it.

Example:

Sender:

1
2
3
4
5

The receiver receives:

1
2
4
5

TCP detects that data is missing.

The sender can retransmit the missing data.

This provides reliability but can also increase delay when packet loss occurs.

11. TCP Flow Control

Flow control prevents the sender from overwhelming the receiver.

For example:

Sender capacity:   Very high
Receiver capacity: Lower

If the sender transmits faster than the receiver can process the data, the receiver could become overwhelmed.

TCP uses a receive window mechanism to communicate how much data the receiver can currently accept.

12. TCP Congestion Control

Flow control protects the receiver.

Congestion control protects the network.

A network can become congested when too much traffic is being transmitted through available links.

TCP responds to congestion by adjusting its sending rate.

Simplified example:

Normal traffic
     ↓
Network congestion detected
     ↓
TCP reduces sending rate
     ↓
Network recovers
     ↓
TCP gradually increases sending rate

This is one reason TCP can behave differently from UDP under network congestion.

13. TCP Connection Termination

TCP normally closes a connection using a four-step process.

Client                         Server

FIN  ----------------------->

     <-------------------- ACK

     <-------------------- FIN

ACK  ----------------------->

The two sides can independently finish sending data because TCP is full-duplex.

The process is:

One side sends FIN.
The other side acknowledges with ACK.
The other side sends its own FIN when it has finished.
The first side sends the final ACK.

This allows both directions of communication to close properly.

14. TCP States

TCP connections can exist in different states.

LISTEN

A server application is waiting for incoming connections.

Example:

Port 443 → LISTEN

This means a service is waiting for clients to connect.

ESTABLISHED

A TCP connection has been successfully established.

Client <--------> Server
       ESTABLISHED

Data can be exchanged.

TIME_WAIT

After a TCP connection closes, one side may remain in TIME_WAIT temporarily.

This helps prevent delayed packets from an old connection from interfering with a future connection.

Other TCP states exist, especially during connection establishment and termination.

15. UDP - User Datagram Protocol

UDP is a connectionless transport protocol.

UDP does not establish a TCP-style connection before sending data.

UDP does not provide TCP's:

Connection establishment
Guaranteed delivery
Ordering
Retransmission
Flow control

UDP is lightweight and has lower protocol overhead.

The application may choose UDP when speed and low delay are more important than perfect delivery.

16. Why UDP Can Be Faster

UDP avoids several mechanisms used by TCP.

TCP normally requires:

Connection establishment
Acknowledgements
Sequence tracking
Retransmissions
Flow control
Congestion control

UDP does not provide these TCP reliability mechanisms.

Therefore, UDP can send data with less protocol overhead and without waiting for retransmissions.

However:

UDP does not guarantee that a network will be fast.

UDP can still experience:

Packet loss
High latency
Jitter
Congestion
Bandwidth limitations
17. UDP and Real-Time Communication

UDP is commonly used for applications where delayed information can be less useful than slightly incomplete information.

Examples include:

Voice communication
Video conferencing
Online gaming
Real-time media
Some streaming and telemetry applications

Example:

If one video packet is lost during a live conversation, the application may continue using newer packets instead of waiting for the old packet to be retransmitted.

The result might be:

A brief visual glitch
A small audio distortion

but communication continues.

For a real-time conversation, waiting several seconds for old data can be worse than losing a small amount of information.

18. Video Streaming and Buffering

UDP does not mean that video can never freeze.

Video can still buffer because of:

Insufficient bandwidth
Packet loss
High latency
Jitter
Wi-Fi interference
Network congestion
Server-side problems
Application problems

Many on-demand video streaming systems use HTTP/HTTPS and therefore commonly operate over TCP or modern HTTP transports that provide reliability.

A video player may download media faster than it plays it and store some data in a buffer.

Example:

Internet → Buffer → Video Player

If data enters the buffer faster than the player consumes it:

Buffer increases

If data arrives slower than the player consumes it:

Buffer decreases
        ↓
Buffer becomes empty
        ↓
Video pauses
        ↓
Loading indicator

Therefore, strong Internet connectivity in terms of advertised bandwidth does not automatically guarantee uninterrupted streaming.

19. TCP vs UDP
Feature	TCP	UDP
Connection	Connection-oriented	Connectionless
Reliability	Reliable	Best effort
Ordering	Yes	Not guaranteed
Retransmission	Yes	No
Acknowledgements	Yes	No
Flow Control	Yes	No
Congestion Control	Yes	Not provided by UDP itself
Overhead	Higher	Lower
Delay	Generally higher	Generally lower
Best suited for	Accuracy and reliability	Speed and real-time communication

Neither protocol is universally better.

The correct choice depends on the application's requirements.

20. Examples of Choosing TCP or UDP
Banking Transaction

TCP is appropriate because:

Data must arrive correctly.
Missing information is unacceptable.
Order matters.
Reliability is more important than minimal delay.
Online Gaming

UDP can be appropriate because:

Current information is more valuable than old information.
Low latency is important.
Small amounts of packet loss may be preferable to waiting for retransmission.
SSH

TCP is appropriate because commands and responses must arrive reliably and in order.

Video Conferencing

UDP is commonly used for real-time media because low delay is important.

21. Transport Layer Troubleshooting

Transport Layer troubleshooting begins after basic connectivity has been established.

A useful troubleshooting sequence is:

1. Is the device connected?
2. Does it have a valid IP configuration?
3. Can it reach the destination?
4. Is the required port reachable?
5. Is the service listening?
6. Is a firewall blocking the connection?
7. Is the TCP connection being established?
8. Are connections being reset or timing out?
9. Is the application itself functioning?
22. Ping Works but the Application Does Not

Example:

User:
"I can ping the server, but I cannot access the website."

A successful ping indicates that basic IP connectivity is working.

However, ping does not prove that the application's TCP port is working.

For example:

Ping → Successful
TCP 443 → Failed

Possible causes include:

Port 443 is blocked.
HTTPS service is not running.
Firewall is blocking TCP 443.
Server is not listening on port 443.
Application is malfunctioning.

This is an important troubleshooting principle:

Successful Layer 3 connectivity does not automatically prove Layer 4 or Layer 7 connectivity.

23. Transport Layer Troubleshooting Commands

Useful commands include:

macOS/Linux
lsof -i

Shows processes using network connections.

Example information can include:

Application/process
Protocol
Local address
Local port
Remote address
Remote port
Connection state
macOS/Linux
netstat

Can display network connections and listening services.

Test a TCP Port
nc -vz <server-ip> <port>

Example:

nc -vz 192.168.1.10 443

Possible result:

succeeded

This indicates that a TCP connection to the specified port could be established.

A failure may indicate:

Port is closed.
Service is not listening.
Firewall is blocking traffic.
Destination is unreachable.
24. Common Transport Layer Problems
Problem 1: Port Blocked

Symptoms:

Device can ping the server.
Application cannot connect.

Possible cause:

Firewall blocking the required port.

Verification:

Test the specific TCP port.

Expected result if working:

Connection succeeded
Problem 2: Service Not Listening

Symptoms:

Server is reachable.
TCP connection to the application port fails.

Possible cause:

The application/service is stopped or not listening on the expected port.

Verification:

Check listening services on the server.

Problem 3: Connection Reset

Symptoms:

Application connects initially.
Connection suddenly terminates.

Possible causes:

Server application closes the connection.
Firewall terminates the session.
Network device interrupts the connection.
Application error.
Problem 4: Connection Timeout

Symptoms:

Application waits for a long time and eventually fails.

Possible causes:

Firewall silently dropping packets.
Destination unavailable.
Routing problem.
Service unavailable.
Problem 5: Packet Loss

Symptoms:

Slow or unstable application.
Retransmissions.
Video or audio problems.
Unstable TCP performance.

Possible causes:

Weak Wi-Fi.
Network congestion.
Faulty physical connection.
Interference.
Overloaded network equipment.
25. Security Threats at the Transport Layer
25.1 SYN Flood

A SYN flood abuses the TCP connection establishment process.

An attacker sends many SYN requests:

SYN
SYN
SYN
SYN
SYN
...

The target may allocate resources for these incomplete connections.

If the attacker sends enough requests, resources can become exhausted.

Impact:

Legitimate users may be unable to establish connections.
Server resources may be consumed.

Defensive mechanisms can include:

SYN cookies.
Rate limiting.
Firewalls.
Intrusion prevention systems.
Traffic monitoring.
26. Port Scanning

Port scanning is the process of probing a host to determine which ports are open, closed, or filtered.

Example:

Port 22  → Open
Port 80  → Closed
Port 443 → Open

An attacker can use this information to identify available services.

Defensive measures include:

Disable unnecessary services.
Restrict exposed ports with firewalls.
Monitor unusual scanning activity.
Use network segmentation.
Keep exposed services secure and updated.

Port scanning is also a legitimate administrative and security testing technique when performed with authorization.

27. TCP Reset Attacks

A TCP reset (RST) terminates a TCP connection.

An attacker may attempt to send forged reset packets to disrupt legitimate connections.

Potential effects:

Users are disconnected.
Long-running sessions are interrupted.

Defensive measures include:

Proper authentication.
Encryption.
Stateful firewalls.
Network monitoring.
Modern protocol protections.
28. UDP Floods

A UDP flood sends a large volume of UDP traffic toward a target.

Potential effects:

Bandwidth exhaustion.
CPU/resource consumption.
Service degradation.
Network congestion.

Defensive measures include:

Rate limiting.
Traffic filtering.
Firewalls.
DDoS protection.
Monitoring.
29. Transport Layer and the OSI Troubleshooting Model

Transport Layer troubleshooting should not happen in isolation.

A network engineer should move through the layers logically.

Layer 1
Physical connectivity
        ↓
Layer 2
MAC addresses, switching, VLANs
        ↓
Layer 3
IP addresses, routing, gateways
        ↓
Layer 4
Ports, TCP, UDP, sessions
        ↓
Layer 7
Application/service

Example:

A user reports:

"I cannot access the company application."

The engineer should not immediately assume the application is broken.

The investigation can proceed:

Layer 1:
Is the device physically/wirelessly connected?

Layer 2:
Is local network communication working?

Layer 3:
Does the device have a valid IP configuration?
Can it reach the server?

Layer 4:
Is the required port reachable?
Is the TCP connection established?

Layer 7:
Is the application/service working?

This prevents troubleshooting from becoming guesswork.

30. Enterprise Relevance

Transport Layer knowledge is important in:

Network Engineering

Engineers use Layer 4 concepts to:

Troubleshoot application connectivity.
Identify blocked ports.
Analyze TCP sessions.
Diagnose packet loss and latency.
System Administration

Administrators use Layer 4 concepts to:

Check listening services.
Configure server applications.
Manage firewalls.
Diagnose connection problems.
Cloud Engineering

Cloud environments use Layer 4 concepts in:

Security groups.
Network access control.
Load balancers.
Firewall rules.
Application connectivity.
Cybersecurity

Security professionals use Layer 4 knowledge for:

Port scanning.
Firewall configuration.
Intrusion detection.
DDoS detection.
Traffic analysis.
Network monitoring.
31. Transport Layer Troubleshooting Mindset

The key principle is:

Do not assume that "the Internet is down" simply because an application is not working.

Separate the problem into layers.

For example:

Ping works
        ↓
Layer 3 probably works

Port 443 fails
        ↓
Investigate Layer 4

Port 443 works
        ↓
Investigate Layer 7

This allows an engineer to narrow down the actual failure point instead of changing random configurations.

32. Key Takeaways
The Transport Layer is Layer 4 of the OSI model.
IP addresses identify devices.
Port numbers identify applications and services.
TCP is connection-oriented and reliable.
UDP is connectionless and optimized for low overhead and low delay.
TCP uses a three-way handshake to establish connections.
TCP uses sequence numbers to track data order.
TCP uses acknowledgements to confirm delivery.
TCP retransmits missing data.
TCP uses flow control to protect the receiver.
TCP uses congestion control to respond to network congestion.
TCP normally uses a four-way process to terminate a connection.
LISTEN means a service is waiting for connections.
ESTABLISHED means a TCP connection is active.
TIME_WAIT is a temporary state after connection termination.
UDP does not guarantee delivery, ordering, or retransmission.
Video calls and real-time applications can use UDP because low delay is important.
Video can still freeze even when UDP is involved because bandwidth, latency, jitter, packet loss, Wi-Fi problems, congestion, and server problems can still occur.
Successful ping does not prove that an application port is working.
Transport Layer troubleshooting focuses on ports, protocols, connections, services, and session behavior.
Important Transport Layer threats include SYN floods, port scanning, TCP reset attacks, and UDP floods.
Transport Layer knowledge connects networking with systems administration, cloud, and cybersecurity. 