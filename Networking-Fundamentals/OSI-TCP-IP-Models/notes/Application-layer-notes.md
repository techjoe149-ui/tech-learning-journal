# Phase 2 — Application Layer Notes

## 1. Application Layer Overview

The Application Layer is the layer closest to the end user.

It provides network services directly to applications such as:

* Web browsers
* Email clients
* DNS utilities
* File transfer applications
* Remote-access applications
* APIs
* Authentication systems

The Application Layer does not mean the graphical application itself. It refers to the **network protocols and services that applications use to communicate**.

Examples include:

```text
HTTP
HTTPS
DNS
SSH
FTP
SMTP
IMAP
POP3
DHCP
```


# 2. Application Layer and the OSI Model

In the OSI model, the Application Layer is:

```text
Layer 7 — Application
```

It is responsible for providing network services to software applications.

The Application Layer communicates with the Presentation and Session layers in the traditional OSI model.

In the TCP/IP model, the functions of:

* Application
* Presentation
* Session

are generally combined into the **Application Layer**.



# 3. Application Layer Responsibilities

The Application Layer provides services such as:

### Resource Access

Allows applications to access network resources.

Example:

```text
Browser → Web server
```

### Name Resolution

Converts human-readable names into IP addresses.

Example:

```text
google.com → IP address
```

### Web Communication

Allows clients and servers to exchange HTTP messages.

Example:

```text
GET / HTTP/2
```

### Authentication

Allows systems to establish the identity of a user or client.

Example:

```text
Username + Password
```

### Authorization

Determines what an authenticated user is allowed to access.

Example:

```text
Employee → HR Portal → Allowed
Employee → Administrator Portal → Denied
```



# 4. Client-Server Model

Many Application Layer protocols use a client-server architecture.

```text
Client
  │
  │ Request
  ▼
Server
  │
  │ Response
  ▼
Client
```

### Client

The device or application requesting a service.

Examples:

* Web browser
* `curl`
* Email client
* SSH client

### Server

The system providing the requested service.

Examples:

* Web server
* DNS server
* Mail server
* SSH server



# 5. DNS

## What is DNS?

DNS stands for:

**Domain Name System**

DNS translates human-readable domain names into IP addresses.

Example:

```text
google.com
     ↓
142.251.x.x
```

Without DNS, users would generally need to know the IP address of every service they wanted to access.



# 6. DNS Resolution

A simplified DNS process is:

```text
User enters:
google.com
     ↓
Client asks DNS resolver
     ↓
DNS resolver finds IP address
     ↓
IP address returned
     ↓
Client connects to destination
```



# 7. DNS Records

Common DNS records include:

| Record | Purpose                              |
| ------ | ------------------------------------ |
| A      | Maps hostname to IPv4 address        |
| AAAA   | Maps hostname to IPv6 address        |
| CNAME  | Alias for another hostname           |
| MX     | Specifies mail servers               |
| NS     | Specifies authoritative name servers |
| TXT    | Stores text-based information        |
| PTR    | Reverse DNS lookup                   |



# 8. DNS Troubleshooting

Useful commands:

```bash
dig google.com
```

and:

```bash
nslookup google.com
```

### Successful DNS response

A successful lookup may contain:

```text
status: NOERROR
```

and an answer section containing an IP address.

### NXDOMAIN

Example:

```text
NXDOMAIN
```

means that the queried domain name does not exist according to the DNS server responding to the query.

### DNS Timeout

A timeout can indicate problems such as:

* DNS server unavailable
* Network connectivity problem
* Firewall filtering
* Incorrect DNS configuration
* Routing problems

DNS failure should be investigated **before moving to TCP or HTTP**, because the client may not know which IP address to contact.

---

# 9. HTTP

HTTP stands for:

**Hypertext Transfer Protocol**

It is one of the most important Application Layer protocols used on the Internet.

HTTP allows clients and servers to exchange requests and responses.

```text
Client
   │
   │ HTTP Request
   ▼
Server
   │
   │ HTTP Response
   ▼
Client
```


# 10. HTTP Request

An HTTP request can contain:

* HTTP method
* URL/path
* Headers
* Optional request body

Example:

```text
GET / HTTP/2
Host: example.com
User-Agent: curl
Accept: */*
```



# 11. HTTP Methods

Common HTTP methods include:

| Method | Purpose                                   |
| ------ | ----------------------------------------- |
| GET    | Retrieve a resource                       |
| POST   | Submit/create data                        |
| PUT    | Replace a resource                        |
| PATCH  | Partially modify a resource               |
| DELETE | Delete a resource                         |
| HEAD   | Request headers without the response body |

The `curl -I` command uses a **HEAD request**.



# 12. HTTP Response

An HTTP response generally contains:

* Status code
* Response headers
* Optional response body

Example:

```text
HTTP/2 200
content-type: text/html
server: ...
```



# 13. HTTP Status Codes

HTTP status codes are grouped into five categories.

| Class | Meaning              |
| ----- | -------------------- |
| 1xx   | Informational        |
| 2xx   | Successful           |
| 3xx   | Redirection          |
| 4xx   | Client/request error |
| 5xx   | Server/service error |



# 14. Important HTTP Status Codes

## 200 — OK

The request was successfully processed.

```text
HTTP/2 200
```

This was demonstrated using:

```bash
curl -I https://example.com
```


## 301 — Moved Permanently

The requested resource has been permanently redirected.

During the lab:

```text
HTTP/2 301
location: https://www.google.com/
```

This was not treated as a connectivity failure.

It demonstrated that the server successfully processed the request and instructed the client to use another URL.



## 400 — Bad Request

The server considered the request invalid or malformed.

Example from the lab:

```text
HTTP/2 400
```

A real `400` investigation may examine:

* URL
* HTTP method
* Headers
* Parameters
* Request body
* Content-Type
* Request syntax

# 15. Authentication and HTTP 401

## Authentication

Authentication answers:

> **Who are you?**

It establishes or verifies the identity of a user or client.

Example:

```text
Username
+
Password
`

## 401 — Unauthorized

A `401 Unauthorized` response generally indicates that authentication is required or that the supplied authentication credentials were not accepted.

During the lab:

```text
HTTP/2 401
WWW-Authenticate: Basic realm="Fake Realm"
```

The `WWW-Authenticate` header provided evidence that the server expected an authentication mechanism.



# 16. HTTP Basic Authentication

Basic Authentication sends credentials using an HTTP `Authorization` header.

Conceptually:

```text
Username + Password
        ↓
Encoding
        ↓
Authorization header
        ↓
Server
```

Using `curl`:

```bash
curl -I -u user:passwd https://httpbingo.org/basic-auth/user/passwd
```

The `-u` option means:

```text
--user
```

and provides the username and password to `curl`.

In the controlled lab, the supplied test credentials changed the response from:

```text
401
```

to:

```text
200
```

This provided experimental evidence that authentication was the cause of the initial failure.

### Security consideration

Real passwords should not normally be placed directly into commands because they may appear in shell history or other local process information.



# 17. Authorization

Authorization is different from authentication.

Authentication:

> **Who are you?**

Authorization:

> **What are you allowed to do?**

Example:

```text
User logs in
      ↓
Authentication
      ↓
Identity confirmed
      ↓
Authorization
      ↓
Access-control policy checked
      ↓
Resource allowed or denied
```



# 18. HTTP 403 — Forbidden

A `403 Forbidden` response indicates that the server is refusing access to the requested resource.

During the lab:

```text
HTTP/2 403
```

The controlled endpoint deliberately produced this response.

A real enterprise investigation would examine:

* User identity
* User role
* Group membership
* Requested resource
* Access-control policy
* Application permissions
* Server/application logs



# 19. 401 vs 403

This distinction is critical.

```text
401
 ↓
Authentication
 ↓
"Who are you?"
```

versus:

```text
403
 ↓
Authorization
 ↓
"Are you allowed?"
```

A useful troubleshooting model is:

```text
User
 ↓
Authentication
 ↓
Identity established
 ↓
Authorization
 ↓
Permission evaluated
 ↓
Resource
```



# 20. HTTPS

HTTPS stands for:

**Hypertext Transfer Protocol Secure**

HTTPS uses HTTP over a secure TLS connection.

Simplified:

```text
HTTP
 +
TLS
 =
HTTPS
```

HTTPS protects communication against interception and provides server authentication through certificates.


# 21. TCP Port 443

HTTPS commonly uses:

```text
TCP 443
```

The normal sequence is:

```text
DNS
 ↓
TCP connection to port 443
 ↓
TLS handshake
 ↓
HTTP communication
```

Port numbers identify services at the transport layer.

The fact that a service uses port `443` does not itself prove that HTTPS is working.

TCP connectivity must first be established, followed by successful TLS negotiation.

---

# 22. TLS

TLS stands for:

**Transport Layer Security**

TLS provides:

* Encryption
* Integrity
* Server authentication

During the HTTPS investigation, the connection successfully negotiated:

```text
TLSv1.3
```



# 23. TLS Handshake

A simplified TLS process is:

```text
Client
  ↓
ClientHello
  ↓
ServerHello
  ↓
Certificate
  ↓
Certificate verification
  ↓
Key establishment
  ↓
Secure session
```

Once TLS is established, HTTP communication can occur securely.


# 24. Digital Certificates

A TLS certificate helps prove that the server is associated with the requested domain.

During the Google investigation, `curl` reported:

```text
SSL certificate verify ok.
```

It also confirmed that the requested hostname matched the certificate's Subject Alternative Name.

This demonstrated successful certificate validation.



# 25. ALPN and HTTP/2

ALPN stands for:

**Application-Layer Protocol Negotiation**

It allows the client and server to agree on an application protocol during TLS negotiation.

During the investigation:

```text
ALPN: server accepted h2
```

and:

```text
using HTTP/2
```

This demonstrated successful negotiation of HTTP/2.



# 26. HTTP/2

HTTP/2 is a newer version of HTTP designed to improve efficiency and performance.

Features include:

* Multiplexing
* Header compression
* Binary framing
* Stream-based communication

A request can therefore appear as:

```text
GET / HTTP/2
```

rather than HTTP/1.1.

---

# 27. `curl` for Application Troubleshooting

`curl` is an important command-line tool for testing HTTP and HTTPS services.

### Headers only

```bash
curl -I https://example.com
```

Useful for quickly examining:

* HTTP status
* Headers
* Server information
* Redirects

### Verbose mode

```bash
curl -v https://example.com
```

Useful for examining:

* DNS resolution
* TCP connection
* TLS handshake
* Certificate information
* HTTP request
* HTTP response

### Authentication

```bash
curl -u username https://example.com
```

Allows `curl` to request a password interactively.



# 28. Application Layer Troubleshooting

A Network Engineer should troubleshoot from the lower dependency toward the application.

A useful sequence is:

```text
DNS
 ↓
TCP
 ↓
TLS
 ↓
HTTP
 ↓
Authentication
 ↓
Authorization
 ↓
Application
```



# 29. Troubleshooting Examples

## DNS Failure

```text
DNS ❌
TCP ?
TLS ?
HTTP ?
```

Investigate:

* DNS server
* DNS configuration
* Resolver
* Network connectivity

Do not jump immediately to HTTP troubleshooting.



## TCP Failure

```text
DNS ✅
TCP ❌
TLS ?
HTTP ?
```

Investigate:

* Routing
* Firewall
* Port accessibility
* Server availability
* Network path



## TLS Failure

```text
DNS ✅
TCP ✅
TLS ❌
HTTP ?
```

Investigate:

* Certificate
* Certificate validity
* Hostname mismatch
* TLS compatibility
* System trust store



## HTTP 4xx

```text
DNS ✅
TCP ✅
TLS ✅
HTTP → 4xx
```

Investigate:

* Request
* Authentication
* Authorization
* URL
* Headers
* Parameters
* Application policy



## HTTP 5xx

```text
DNS ✅
TCP ✅
TLS ✅
HTTP → 5xx
```

Investigate:

* Server
* Backend
* Application
* Load balancer
* Service availability



# 30. Fault Isolation

A successful connection at one layer does not prove that every higher layer is functioning.

For example:

```text
TCP 443 succeeds
```

does not automatically mean:

```text
TLS works
```

and:

```text
TLS succeeds
```

does not automatically mean:

```text
Authentication succeeds
```

Therefore, troubleshooting must proceed step-by-step.



# 31. Client-Side vs Server-Side Problems

One of the most important lessons from the HTTPBin investigation was distinguishing a client problem from an external service problem.

Example:

```text
HTTPBin → 503
example.com → 200
```

This comparison provided evidence that general HTTPS connectivity was functioning.

The likely fault domain therefore moved toward:

```text
HTTPBin service/infrastructure
```

rather than:

```text
Client DNS
Client TCP
Client TLS
Client HTTPS
```

The exact backend cause was not established.



# 32. Do Not Fix What Isn't Broken

A professional troubleshooting principle is:

> **Do not modify a component until evidence indicates that it is responsible for the failure.**

If:

```text
DNS ✅
TCP ✅
TLS ✅
HTTP ✅
```

and the server returns:

```text
503
```

changing the client's DNS configuration without evidence is unnecessary.

Instead:

* Document the evidence.
* Isolate the fault domain.
* Escalate if appropriate.
* Monitor.
* Retest.



# 33. Application Layer Security

Security attacks will be covered in greater depth during the dedicated security phase.

At the Application Layer, the important fundamentals are:

* Authentication
* Authorization
* Secure HTTPS communication
* Certificate validation
* Secure handling of credentials
* Understanding application responses

The purpose of Phase 2 is to understand **how the application layer works and how to troubleshoot it**, rather than exhaustively studying application-layer attacks.



# 34. Practical Commands Learned

```bash
dig google.com
```

```bash
nslookup google.com
```

```bash
nc -vz example.com 443
```

```bash
curl -I https://example.com
```

```bash
curl -v https://example.com
```

```bash
curl -I https://httpbingo.org/status/400
```

```bash
curl -I https://httpbingo.org/status/403
```

```bash
curl -I https://httpbingo.org/basic-auth/user/passwd
```

```bash
curl -I -u user:passwd https://httpbingo.org/basic-auth/user/passwd
```



# 35. Application Layer Troubleshooting Checklist

When a user reports that an application is unavailable:

### Step 1 — DNS

```bash
dig <domain>
```

Confirm the hostname resolves.

### Step 2 — TCP

```bash
nc -vz <domain> 443
```

Confirm TCP/443 connectivity.

### Step 3 — HTTPS/TLS

```bash
curl -I https://<domain>
```

Confirm that the HTTPS service responds.

### Step 4 — Detailed investigation

```bash
curl -v https://<domain>
```

Use only after checking whether the output could expose sensitive information.

### Step 5 — Interpret HTTP status

```text
2xx → Success
3xx → Redirect
4xx → Request/auth/access problem
5xx → Server/service problem
```

### Step 6 — Authentication

If:

```text
401
```

investigate credentials and authentication mechanisms.

### Step 7 — Authorization

If:

```text
403
```

investigate roles, permissions, and access-control policies.

### Step 8 — Remediate

Apply the correction appropriate to the identified fault domain.

### Step 9 — Verify

Repeat the failed test.

### Step 10 — Document

Record:

* Symptom
* Evidence
* Diagnosis
* Action
* Result
* Final verification


# 36. Application Layer Lab Summary

The practical labs demonstrated:

```text
DNS Investigation
        ↓
HTTP/HTTPS Investigation
        ↓
Authentication Investigation
        ↓
Authorization Investigation
        ↓
End-to-End Application Troubleshooting
```

The labs used actual command-line tools and controlled public services to demonstrate the concepts.



# 37. Key Takeaways

The most important lessons from the Application Layer are:

1. **DNS converts names into addresses.**
2. **TCP provides the transport connection used by many application protocols.**
3. **HTTPS combines HTTP with TLS.**
4. **TLS provides encryption, integrity, and server authentication.**
5. **Certificates help authenticate the server's identity.**
6. **HTTP status codes provide valuable troubleshooting evidence.**
7. **401 relates primarily to authentication.**
8. **403 relates primarily to authorization/access denial.**
9. **4xx responses require investigation of the request/client interaction.**
10. **5xx responses generally shift investigation toward the service/server side.**
11. **A successful lower-layer test does not guarantee application success.**
12. **Troubleshooting should follow evidence rather than assumptions.**
13. **Do not change a functioning component without evidence that it is responsible.**
14. **Authentication and authorization are separate security controls.**
15. **Verbose troubleshooting output should be checked for sensitive information before screenshots are published.**



# Conclusion

The Application Layer connects network infrastructure to the services users actually interact with.

Through the Phase 2 Application Layer work, I learned how DNS resolution, TCP connectivity, TLS, HTTP, authentication, authorization, and application responses fit together.

More importantly, I learned how to troubleshoot an application systematically rather than simply assuming that a failed website means a network failure.

The practical methodology developed throughout this phase is:

```text
Detect
  ↓
Isolate
  ↓
Confirm
  ↓
Remediate
  ↓
Verify
  ↓
Document
```

This approach allows a Network Engineer to identify the actual fault domain, avoid unnecessary configuration changes, and provide evidence-based troubleshooting.

