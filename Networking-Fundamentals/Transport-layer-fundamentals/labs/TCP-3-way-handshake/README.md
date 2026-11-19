
Transport Fundamentals — TCP Handshake Lab

Phase: Transport Fundamentals
Lesson: Lesson 10 — TCP Handshake Lab
Status: Completed

1. Objective

To capture and identify the TCP three-way handshake in real network traffic and connect the observed packets to the concepts learned in TCP fundamentals.

The lab focused on identifying:

SYN
SYN-ACK
ACK
Source and destination ports
Sequence numbers
Acknowledgement numbers
The transition from connection establishment to data exchange

2. Lab Environment
Operating System: macOS
Network interface: en0
Tools: Terminal, tcpdump, curl
Protocol: TCP
Target: HTTPS web server
Destination service port: 443

Machine-specific network addresses and ephemeral ports have been removed from this public documentation.

3. Concept

TCP is a connection-oriented transport protocol.

Before normal application data is exchanged, TCP establishes a logical connection between two transport endpoints using the three-way handshake:

SYN → SYN-ACK → ACK

The handshake allows both endpoints to establish and synchronize their TCP communication state.

4. Procedure
Step 1 — Start packet capture

The following command was used to capture TCP traffic involving the target:

sudo tcpdump -ni en0 'tcp and host example.com'

tcpdump began listening for matching TCP traffic.

Step 2 — Generate TCP traffic

A separate Terminal window was used to create an HTTPS connection:

curl -I https://example.com

This generated TCP traffic to the web server.

Step 3 — Stop the capture

After the connection and data exchange occurred, the capture was stopped using:

Control + C

5. Observed Three-Way Handshake

The first three packets belonging to the TCP connection were:

Packet 1 — SYN
<CLIENT-IP>:<EPHEMERAL-PORT> > <SERVER-IP>:443: Flags [S], seq <CLIENT-INITIAL-SEQ>

Interpretation:

[S] = SYN
The client initiated the TCP connection.
The client provided an initial sequence number.
Port 443 identified the HTTPS service endpoint.

Conceptually:

Client → Server
        SYN
Packet 2 — SYN-ACK
<SERVER-IP>:443 > <CLIENT-IP>:<EPHEMERAL-PORT>: Flags [S.], seq <SERVER-INITIAL-SEQ>, ack <NEXT-EXPECTED>

Interpretation:

[S.] = SYN + ACK
The server responded to the client's SYN.
The server provided its own initial sequence number.
The acknowledgement number acknowledged the client's SYN.

Conceptually:

Client ← Server
      SYN-ACK

An important observation was that the acknowledgement number was one greater than the client's SYN sequence number.

This occurs because a SYN consumes one sequence-number position.

Packet 3 — ACK
<CLIENT-IP>:<EPHEMERAL-PORT> > <SERVER-IP>:443: Flags [.], ack <ACK>

Interpretation:

[.] = ACK
The client acknowledged the server's SYN-ACK.
The three-way handshake was completed.

Conceptually:

Client → Server
        ACK
6. Handshake Summary

The captured traffic demonstrated:

Client                         Server

   SYN ---------------------->

       <---------------- SYN-ACK

   ACK ---------------------->

       CONNECTION ESTABLISHED

   Data --------------------->

After the third packet, TCP data segments appeared in the capture.

This demonstrated that normal application data followed the successful establishment of the TCP connection.

7. Important Observations
Source and destination ports

The client used an ephemeral source port while the server used destination port 443.

<CLIENT-IP>:<EPHEMERAL-PORT>
              ↓
       <SERVER-IP>:443

This reinforced the earlier lesson that source and destination port roles depend on the direction of communication.

TCP flags

The capture showed:

[S]   → SYN
[S.]  → SYN + ACK
[.]   → ACK
Sequence numbers

The SYN packets contained initial sequence numbers used by TCP to establish sequence tracking for the connection.

Acknowledgement numbers

The server's acknowledgement of the client's SYN demonstrated that TCP uses acknowledgement numbers to indicate what has been received and what is expected next.

Data followed the handshake

After:

SYN → SYN-ACK → ACK

the capture showed TCP segments containing application data.

This provided practical evidence for the concept:

Establish → Communicate → Terminate
8. Troubleshooting / Problem-Solving Process

Problem: Observe a TCP connection being established in real network traffic.

Approach:

Select the active network interface.
Start tcpdump.
Generate controlled TCP traffic using curl.
Identify the first three packets belonging to the connection.
Examine the TCP flags.
Compare the sequence and acknowledgement numbers.
Observe data exchange after the handshake.

Result: The complete three-way handshake was successfully captured and identified.

Cross-Disciplinary Integration

The TCP three-way handshake is not an isolated networking concept. It is a foundational mechanism that appears throughout modern IT infrastructure.

8.1 ☁️ Cloud Computing

Cloud applications constantly establish TCP connections between systems.

Examples include:

A client connecting to a cloud-hosted web server.
An application connecting to a database.
Communication between application servers.
Connections between clients and cloud APIs.
Applications communicating through cloud load-balancing infrastructure.
Practical Connection

If a cloud application cannot connect to a service on TCP port 443, understanding the handshake helps determine whether the problem occurs during connection establishment or later during application communication.

For example:

Client
   │
   │ SYN
   ↓
Cloud Service
   │
   │ SYN-ACK
   ↓
Client
   │
   │ ACK
   ↓
Connection Established

A failure to receive the expected response can indicate a connectivity, routing, filtering, or service-availability problem.

Future Career Relevance

This knowledge becomes useful when working with:

Cloud infrastructure
Cloud networking
Cloud support
DevOps
Site Reliability Engineering
8.2 ⚙️ Automation

TCP connectivity can be tested and monitored automatically.

For example, an automation script can check whether a service is accepting TCP connections on an expected port.

The conceptual workflow is:

Automation Script
       ↓
Attempt TCP Connection
       ↓
Connection Successful?
       ↓
Yes → Service reachable
No  → Investigate

Later, Python can be used to automate network checks, collect results, generate reports, and trigger alerts.

Connection to This Learning Roadmap
Networking
    ↓
Understand TCP
    ↓
Python
    ↓
Automate Network Checks
    ↓
Infrastructure Monitoring

The TCP handshake therefore provides knowledge that can later be used in practical automation rather than learning Python networking commands in isolation.

8.3 🔐 Cybersecurity

The TCP handshake is important for understanding and analyzing network behavior.

Security analysts may examine TCP connection attempts when investigating:

Unexpected network connections
Repeated connection attempts
Port scanning
Suspicious services
Network reconnaissance
Malicious or abnormal communication patterns

Understanding what a normal TCP connection looks like is necessary before identifying abnormal behavior.

For example:

Normal:

SYN → SYN-ACK → ACK
       ↓
Connection established


Potentially suspicious pattern:

SYN → SYN → SYN → SYN → ...

The second pattern could indicate repeated connection attempts and would require further investigation.


9. Career & Job Relevance
Skills Learned
TCP connection establishment
TCP three-way handshake
TCP flags
Source and destination ports
Sequence numbers
Acknowledgement numbers
Basic packet capture
Basic network traffic analysis
Using tcpdump for troubleshooting

Job Titles That Use These Skills:
Network Support Technician
Network Administrator
NOC Analyst
Network Engineer
Systems Administrator
SOC Analyst
Cybersecurity Analyst
Real Workplace Scenarios

These concepts are useful when:

Investigating why a TCP service cannot establish connections.
Determining whether a server is accepting TCP connections.
Troubleshooting application connectivity.
Examining suspicious or unexpected network traffic.
Diagnosing network problems using packet captures.
Verifying whether a service is communicating over the expected port.
How They Appear in Job Descriptions

You may encounter requirements such as:

"Troubleshoot TCP/IP connectivity issues."
"Analyze network traffic using packet capture tools."
"Understand TCP/IP protocols and network services."
"Monitor and troubleshoot network communications."
"Use tools such as Wireshark or tcpdump for network analysis."

10. Privacy & GitHub Safety

The original capture contained machine-specific information including:

Private IP addresses
Remote IP address
Ephemeral source port
Sequence numbers
Timestamps
TCP connection details

These values are not necessary to demonstrate understanding and have therefore been generalized in this public documentation.

The lab demonstrates the process and technical reasoning, rather than exposing the user's actual network information.

11. Exit Criteria

Before considering this lab complete, I am able to:

Explain why TCP establishes a connection.

Identify a SYN packet.

Identify a SYN-ACK packet.

Identify an ACK packet.

Explain the three-way handshake.

Identify source and destination ports.

Explain the basic role of sequence numbers.

Explain the basic role of acknowledgement numbers.

Use tcpdump to observe TCP traffic.

Recognize that application data follows successful connection establishment.
