# Transport Layer Incident Report

## Incident 001 — Internal HR Portal Inaccessible

## 1. Incident Summary

### Incident Description

A user reported being unable to access the organization's internal HR portal while confirming that general Internet access and other websites were functioning normally.

The objective of the investigation was to determine whether the problem originated from:

* The user's network connection
* Layer 2 connectivity
* IP configuration
* Routing
* Transport Layer connectivity
* The HR service
* HTTPS/TLS
* Authentication or authorization
* Application-level access controls

The investigation followed a systematic, layered troubleshooting methodology.



# 2. User Report

The user reported:

> "I can access the network and other websites, but I cannot access the company's HR portal."

Additional information:

* Wi-Fi was connected.
* Other websites were accessible.
* The browser was functioning.
* The HR portal had worked previously.
* Other employees were reportedly able to access the HR portal.



# 3. Known Application Information

The organization provided the following application information:

```text
Application:       Internal HR Portal
Hostname:          hr.company.local
Protocol:          HTTPS
Transport:         TCP
Destination Port:  443
```

This information allowed the investigation to move from general connectivity testing toward a specific Transport Layer test.



# 4. Investigation Methodology

The investigation followed a bottom-up troubleshooting approach.

```text
Layer 1
Physical / Interface
        ↓
Layer 2
Local Network
        ↓
Layer 3
IP Connectivity
        ↓
Layer 4
TCP Connectivity
        ↓
Application
HTTPS / Access Control
```

The objective was to eliminate working layers using evidence rather than assuming the cause.



# 5. Step 1 — Verify Network Interface

The first check was to confirm that the user's network interface was operational.

Example command:

```bash
ifconfig en0
```

Relevant information:

```text
status: active
inet 192.168.10.25
```

### Interpretation

The network interface was active and had an IPv4 address.

This indicated that:

* The interface was operational.
* The device was connected to the network.
* An IPv4 address had been assigned.

### Result

**PASS**

Layer 1/interface availability was not the immediate cause of the incident.



# 6. Step 2 — Verify IP Configuration

The network configuration was identified as:

```text
IP Address:     192.168.10.25
Subnet Mask:    255.255.255.0
Default Gateway: 192.168.10.1
```

The configuration was consistent with the local network.

### Result

**PASS**

The device had a usable IPv4 configuration.



# 7. Step 3 — Test Default Gateway

The default gateway was tested using:

```bash
ping 192.168.10.1
```

The gateway responded successfully.

### Interpretation

The successful response demonstrated that the user's device could communicate with the local gateway.

This provided evidence that local network connectivity was functioning.

### Result

**PASS**

No immediate Layer 2/Layer 3 gateway connectivity problem was identified.



# 8. Step 4 — Test External Connectivity

External connectivity was tested with:

```bash
ping google.com
```

Successful replies were received.

### Interpretation

This demonstrated that:

* The device could reach an external destination.
* The default gateway was forwarding traffic.
* Basic IP connectivity was functioning.
* General Internet access was available.

### Result

**PASS**

The user's statement that other websites worked was supported by testing.



# 9. Step 5 — Identify the Required Transport Service

The HR application was identified as:

```text
Protocol:          HTTPS
Transport:         TCP
Destination Port: 443
```

The investigation therefore needed to determine whether the user could establish a TCP connection to:

```text
hr.company.local:443
```



# 10. Step 6 — Test TCP Connectivity

The following command was selected:

```bash
nc -vz hr.company.local 443
```

### Result

```text
Connection to hr.company.local port 443 [tcp/https] succeeded!
```

### Interpretation

The TCP connection was successfully established.

This demonstrated that:

* The destination was reachable at the Transport Layer.
* TCP communication was functioning.
* Port 443 was accessible.
* A service was accepting TCP connections on the destination port.

### Result

**PASS**

No immediate Transport Layer connectivity failure was identified.



# 11. Step 7 — Continue Above the Transport Layer

Because TCP connectivity was successful, the investigation should not continue treating the problem as a basic Layer 4 failure.

The next question became:

> Can the HTTPS service actually process and authorize the user's request?

An HTTPS-level test was therefore performed.

Command:

```bash
curl -I https://hr.company.local
```



# 12. Step 8 — Analyze HTTPS Response

The server returned:

```text
HTTP/1.1 403 Forbidden
```

### Interpretation

The request successfully reached the web server.

However, the server refused to authorize the requested resource.

This was a critical finding.

The problem was no longer best explained by:

* Wi-Fi failure
* IP addressing failure
* Gateway failure
* General routing failure
* TCP port 443 being inaccessible

Instead, the investigation moved toward the application and access-control layers.



# 13. Layer-by-Layer Elimination

| Layer / Component     | Evidence                     | Status             |
| --------------------- | ---------------------------- | ------------------ |
| Network Interface     | Interface active             | PASS               |
| IP Configuration      | Valid IPv4 configuration     | PASS               |
| Local Gateway         | Gateway responds             | PASS               |
| Internet Connectivity | Google reachable             | PASS               |
| TCP                   | Port 443 connection succeeds | PASS               |
| HTTPS                 | Server responds              | PASS               |
| Application Access    | HTTP 403                     | FAIL / INVESTIGATE |

The investigation therefore isolated the problem to the **application/access-control area**, rather than basic network connectivity.



# 14. Root-Cause Area

The evidence points toward an **application-layer access-control problem**.

Potential causes include:

### Authentication

The user's authentication session may have:

* Expired.
* Failed.
* Not been established correctly.

### Authorization

The user's account may lack the required permission or role.

For example:

```text
User
 ↓
Authentication
 ↓
Identity confirmed
 ↓
Authorization
 ↓
Access denied
```

### Application Access Policy

The HR application may enforce policies based on:

* User group
* Department
* Source IP
* Network location
* Device
* Security policy

### Application Configuration

The application may have an incorrectly configured access rule.

### Server/Application Logs

Application logs should be examined to determine exactly why the request generated HTTP 403.


# 15. Recommended Administrative Investigation

The application administrator should investigate in the following order:

### 1. Verify the User Account

Check:

* Account status
* Authentication state
* Password/credential status
* Session validity

### 2. Verify Authorization

Check:

* User role
* Department membership
* Application permissions
* Access-control groups

### 3. Check Application Policies

Determine whether access is restricted based on:

* IP address
* VLAN
* Network location
* Device
* User group

### 4. Review Application Logs

Search for the affected user's request and identify the reason for the `403 Forbidden` response.

### 5. Compare With a Working User

If another employee can access the portal, compare:

```text
User account
Permissions
Device
Network
Browser/session
Application configuration
```

This comparison can help isolate a user-specific problem.



# 16. Why the Firewall Was Not the First Suspect

A firewall can still affect application communication, but the available evidence made a basic TCP firewall block less likely.

The test:

```bash
nc -vz hr.company.local 443
```

succeeded.

Therefore:

```text
Client
   ↓
TCP 443
   ↓
HR Server
```

was reachable.

The subsequent HTTP response:

```text
403 Forbidden
```

also demonstrated that the request reached the web server and received an application-level response.

Therefore, the investigation should prioritize application access controls before assuming a basic Layer 4 firewall block.



# 17. Troubleshooting Evidence Chain

The investigation can be summarized as:

```text
User cannot access HR portal
            ↓
Wi-Fi/interface checked
            ↓
Interface active
            ↓
IP configuration valid
            ↓
Gateway reachable
            ↓
Internet reachable
            ↓
HR server TCP/443 reachable
            ↓
HTTPS request reaches server
            ↓
HTTP 403 Forbidden
            ↓
Network connectivity eliminated
            ↓
Investigate application access control
```



# 18. Final Incident Assessment

### Finding

The investigation did not identify a Layer 1, Layer 2, Layer 3, or basic Transport Layer connectivity failure.

The user's device successfully:

* Connected to the network.
* Obtained a valid IP configuration.
* Reached the default gateway.
* Reached external Internet destinations.
* Established a TCP connection to the HR server on port 443.

The HR server subsequently returned:

```text
HTTP 403 Forbidden
```

This indicates that the request reached the server but access was denied.

### Most Likely Root-Cause Area

**Application-layer authentication, authorization, or access-control policy.**

A definitive root cause would require access to the HR application's logs and configuration.



# 19. Recommended Resolution

The application administrator should:

1. Verify the user's account status.
2. Verify the user's HR application permissions.
3. Confirm the user belongs to the correct access-control group.
4. Check authentication/session status.
5. Review HR application logs.
6. Check application access policies.
7. Compare the affected user with a working user.
8. Correct the relevant application permission or policy.
9. Retest access from the affected device.



# 20. Verification After Remediation

After the administrator makes the appropriate correction, the user should retest:

```text
1. Open the HR portal.
2. Authenticate.
3. Confirm the application loads.
4. Confirm the required HR functions work.
```

The engineer should document:

```text
Previous result:
HTTP 403 Forbidden

Expected result after remediation:
Successful authenticated application access
```



# 21. Security Considerations

The incident demonstrates that network connectivity and application authorization are separate controls.

A server can be:

```text
Reachable
+
TCP port open
+
HTTPS responding
```

while still denying access to a particular user.

This is an important enterprise security principle:

> **Network reachability does not equal application authorization.**

Security controls may exist at multiple levels:

```text
Network Firewall
       ↓
ACL
       ↓
Server Firewall
       ↓
TLS
       ↓
Authentication
       ↓
Authorization
       ↓
Application Access Control
```



# 22. Lessons Learned

This incident reinforced several professional troubleshooting principles.

### Do not assume the user's description identifies the failing layer.

The user reported an application problem, but the engineer still verified the lower layers.

### Do not stop at ping.

A successful ping only demonstrates IP-level reachability.

### Test the actual service.

Testing:

```bash
nc -vz hr.company.local 443
```

was more relevant than simply testing whether the server responded to ICMP.

### Interpret failures carefully.

A timeout, connection refusal, and HTTP 403 represent different failure conditions.

### Move upward when lower layers pass.

Once TCP connectivity was proven, continued investigation had to move toward HTTPS and the application.

### Document evidence.

Every troubleshooting conclusion should be supported by an observed result.



# 23. Skills Demonstrated

This incident demonstrates practical ability to:

* Investigate enterprise connectivity complaints.
* Follow a structured troubleshooting methodology.
* Verify network interfaces.
* Validate IP configuration.
* Test gateway connectivity.
* Test external connectivity.
* Identify application transport requirements.
* Test TCP ports.
* Interpret TCP connectivity results.
* Perform HTTPS-level testing.
* Interpret HTTP status codes.
* Isolate failures by layer.
* Identify application-layer access-control problems.
* Recommend appropriate escalation.
* Document an incident professionally.



# 24. Final Conclusion

The HR portal incident was investigated systematically from the network interface through the Transport Layer and into the application.

The evidence showed:

```text
Interface              → PASS
IP Configuration       → PASS
Gateway Connectivity   → PASS
Internet Connectivity  → PASS
TCP/443 Connectivity   → PASS
HTTPS Communication    → PASS
Application Access     → DENIED
```

The investigation therefore concluded that the available evidence did not support a basic network or Transport Layer failure.

The most likely problem area was application-level access control, requiring further investigation of authentication, authorization, permissions, application policies, and server logs.

The key professional lesson from this project is:

> **Troubleshoot from evidence, not assumptions. Identify what works, eliminate those components, isolate what remains, and escalate with a clear technical explanation.**
