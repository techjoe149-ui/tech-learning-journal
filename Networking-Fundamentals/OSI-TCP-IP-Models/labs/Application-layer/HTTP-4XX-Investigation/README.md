# Lab 02 — HTTP/HTTPS Investigation

## Objective

Investigate HTTP and HTTPS communication from a real macOS environment and develop a structured approach to troubleshooting web connectivity and application-layer failures.

The lab examines the communication path from DNS resolution through TCP, TLS, HTTP/2, and HTTP response codes.

The investigation follows the engineering workflow:

```text
Detect → Isolate → Confirm → Remediate → Verify → Document
```

Where a real remediation cannot safely be performed because the fault is external, the appropriate response is documented as escalation, monitoring, and retesting.

---

# Concepts Covered

* HTTP and HTTPS
* TCP port 443
* TLS
* TLS 1.3
* Digital certificates
* Certificate validation
* ALPN
* HTTP/2
* HTTP status codes
* `2xx` success responses
* `3xx` redirects
* `4xx` client/request errors
* `5xx` server/service errors
* HTTP `301`
* HTTP `400`
* HTTP `503`
* `curl`
* `nc`
* Fault isolation
* Client-side vs server-side troubleshooting

---

# Network Environment

| Item             | Details     |
| ---------------- | ----------- |
| Operating System | macOS       |
| Client           | MacBook Pro |
| Primary Tool     | `curl`      |
| TCP Testing Tool | `nc`        |
| HTTPS Port       | 443         |

> **Security note:** Before publishing screenshots, check verbose output for private IP addresses, internal hostnames, credentials, cookies, tokens, or authentication headers. Public destination information such as Google certificate details is generally safe for this learning project.

---

# HTTPS Communication Model

The investigation follows this sequence:

```text
DNS Resolution
      ↓
TCP Connection
      ↓
TLS Handshake
      ↓
Certificate Validation
      ↓
HTTP/2 Negotiation
      ↓
HTTP Request
      ↓
HTTP Response
      ↓
Application Processing
```

The purpose of the lab is to determine how far communication progresses and where a failure occurs.

---

# Test 1 — TCP Connectivity to HTTPS

## Command

```bash
nc -vz google.com 443
```

## Purpose

Determine whether the client can establish a TCP connection to the HTTPS service on port 443.

## Observed Result

The connection succeeded.

## Interpretation

The client successfully established a TCP connection to port 443 on the destination.

## Diagnosis

TCP connectivity to the HTTPS service was functioning.

This test establishes connectivity at the transport layer but does **not** prove that:

* TLS works
* The certificate is valid
* HTTP works
* Authentication succeeds
* Authorization succeeds
* The application works

Therefore, further testing is required.

---

# Test 2 — HTTPS/TLS and HTTP Investigation

## Command

```bash
curl -v https://google.com
```

## Purpose

Investigate the complete HTTPS communication process.

The test examines:

* DNS resolution
* TCP connectivity
* TLS handshake
* Certificate validation
* HTTP/2 negotiation
* HTTP request
* HTTP response

---

## 2.1 DNS Resolution

The output showed:

```text
Host google.com:443 was resolved.
IPv4: 142.251.37.142
```

### Interpretation

The hostname was successfully resolved to an IPv4 address.

### Diagnosis

DNS resolution succeeded.



## 2.2 TCP Connection

The output showed:

```text
Connected to google.com (142.251.37.142) port 443
```

### Interpretation

The client successfully established a TCP connection with Google's HTTPS service on port 443.

### Diagnosis

TCP connectivity succeeded.



## 2.3 TLS Handshake

The output showed:

```text
TLS handshake, Client hello
TLS handshake, Server hello
TLS handshake, Certificate
TLS handshake, CERT verify
TLS handshake, Finished
```

The connection then reported:

```text
SSL connection using TLSv1.3
```

### Interpretation

The TLS handshake completed successfully and TLS 1.3 was negotiated.

### Diagnosis

TLS negotiation succeeded.



## 2.4 Certificate Validation

The certificate information included:

```text
subject: CN=*.google.com
```

The hostname was successfully matched:

```text
subjectAltName: host "google.com" matched cert's "google.com"
```

The validation result was:

```text
SSL certificate verify ok.
```

### Interpretation

The server certificate was trusted and the hostname matched the certificate.

### Diagnosis

Certificate validation succeeded.



## 2.5 HTTP/2 Negotiation

The output showed:

```text
ALPN: server accepted h2
using HTTP/2
```

### Interpretation

ALPN successfully negotiated HTTP/2 between the client and server.

### Diagnosis

HTTP/2 negotiation succeeded.



## 2.6 HTTP Request

The client sent:

```text
GET / HTTP/2
Host: google.com
User-Agent: curl/8.7.1
Accept: */*
```

The output confirmed:

```text
Request completely sent off
```

### Interpretation

The HTTP request was successfully constructed and transmitted.

### Diagnosis

The HTTP request reached the server.



## 2.7 HTTP Response

The server returned:

```text
HTTP/2 301
```

with:

```text
location: https://www.google.com/
```

### Interpretation

HTTP `301` means **Moved Permanently**.

The server successfully processed the request but instructed the client to use another URL.

### Diagnosis

The `301` response was a valid HTTP response and was **not a connectivity failure**.


# Test 3 — HTTP 503 Investigation and Fault Isolation

## Objective

Investigate an unexpected `503 Service Unavailable` response and determine whether the problem originates from the client or the remote service.


## 3.1 Initial Request

### Command

```bash
curl -I https://httpbin.org/status/404
```

### Observed Result

```text
HTTP/2 503
server: awselb/2.0
content-type: text/html
content-length: 162
```

### Interpretation

The service returned HTTP `503 Service Unavailable` rather than the expected `404`.

The `server: awselb/2.0` header indicates that an AWS Elastic Load Balancer was involved in generating the response.

The exact backend cause cannot be determined from the response alone.



## 3.2 Compare Another HTTPBin Path

### Command

```bash
curl -I https://httpbin.org/
```

### Observed Result

The root path returned the same:

```text
HTTP/2 503
server: awselb/2.0
```

### Interpretation

A different path on the same service also returned `503`.

This reduces the likelihood that the original `/status/404` endpoint alone was responsible for the failure.

The evidence instead points toward a broader service or infrastructure availability problem.



## 3.3 Independent Service Comparison

### Command

```bash
curl -I https://example.com
```

### Observed Result

```text
HTTP/2 200
```

### Interpretation

A separate public HTTPS service successfully returned `200 OK`.

This provides an independent comparison and demonstrates that HTTPS communication from the client was functioning normally.


# Fault Isolation

The results were:

| Destination              | Result                    |
| ------------------------ | ------------------------- |
| `httpbin.org/status/404` | `503 Service Unavailable` |
| `httpbin.org/`           | `503 Service Unavailable` |
| `example.com/`           | `200 OK`                  |

The evidence can be represented as:

```text
Client
   ↓
Internet connectivity        ✅
   ↓
HTTPS communication           ✅
   ↓
example.com                   → 200 ✅
   ↓
httpbin.org                   → 503 ⚠️
   ↓
Multiple HTTPBin paths        → 503 ⚠️
```

### Diagnosis

The evidence indicates that the fault was most likely within the HTTPBin service or its supporting infrastructure rather than the client's basic network connectivity.

The exact backend cause was not established.


# Remediation — HTTP 503

No client-side configuration change was required.

The appropriate engineering response to an external service fault would be:

1. Document the observed response.
2. Record the affected service and timestamp.
3. Confirm independent services remain reachable.
4. Escalate or report the issue if operating within an organization.
5. Monitor the service.
6. Retest after recovery.

### Engineering principle

> **Do not modify a functioning component when evidence points to an external fault.**

The investigation therefore demonstrated that remediation does not always mean changing the client.

Sometimes the correct remediation is **escalation, monitoring, and verification**.



# Test 4 — HTTP 400 Investigation

## Command

```bash
curl -I https://httpbin.org/status/400
```

## Purpose

Demonstrate and interpret a controlled HTTP `400 Bad Request` response.

This test was intentionally generated using a public testing endpoint.



## Observed Result

```text
HTTP/2 400
date: Wed, 12 Aug 2026 08:02:24 GMT
content-type: text/html; charset=utf-8
content-length: 0
server: gunicorn/19.9.0
access-control-allow-origin: *
access-control-allow-credentials: true
```

## Interpretation

HTTP `400 Bad Request` indicates that the server received the HTTP request but considered the request invalid or malformed.

The request reached the HTTP service far enough for the server to generate a response.

Therefore, this response does not indicate:

* DNS failure
* TCP connection failure
* TLS failure
* Complete server unavailability



# 400 Troubleshooting Workflow

For a real HTTP `400` response, an engineer would investigate the request itself.

Potential areas include:

```text
URL/path
   ↓
HTTP method
   ↓
Headers
   ↓
Parameters
   ↓
Request body
   ↓
Content-Type
   ↓
Malformed request data
```

The general remediation process would be:

```text
400 Bad Request
      ↓
Inspect request
      ↓
Identify invalid component
      ↓
Correct request
      ↓
Send request again
      ↓
Verify successful response
```

Because this lab used a controlled endpoint specifically designed to return `400`, no real malformed-request remediation was performed.

The test therefore demonstrates **fault recognition and troubleshooting methodology**, rather than a real-world client repair.



# HTTP Status Code Comparison

The lab demonstrated three different HTTP response classes:

| Status | Class | Meaning                    | Investigation               |
| ------ | ----- | -------------------------- | --------------------------- |
| `200`  | 2xx   | Successful request         | Continue normally           |
| `301`  | 3xx   | Resource redirected        | Follow/check redirect       |
| `400`  | 4xx   | Request considered invalid | Inspect client request      |
| `503`  | 5xx   | Service unavailable        | Investigate service/backend |

These status codes should be treated as **evidence**, not automatic proof of the exact root cause.



# End-to-End Troubleshooting Model

The lab demonstrated the following troubleshooting hierarchy:

```text
DNS
 ↓
TCP
 ↓
TLS
 ↓
Certificate Validation
 ↓
HTTP/2
 ↓
HTTP Request
 ↓
HTTP Response
 ↓
Application
```

When a failure occurs, the engineer should identify the **lowest stage that failed** before changing anything.

For example:

```text
DNS failure
→ Investigate DNS

TCP failure
→ Investigate connectivity, routing, firewall, or port

TLS failure
→ Investigate certificates or TLS configuration

HTTP 4xx
→ Investigate request, authentication, or authorization

HTTP 5xx
→ Investigate server/application/service availability
```

Further evidence should always be collected before assigning a final root cause.



# Troubleshooting Method Applied

The laboratory followed:

```text
Detect
  ↓
Identify the symptom
  ↓
Isolate
  ↓
Compare possible fault domains
  ↓
Confirm
  ↓
Determine the most likely fault area
  ↓
Remediate
  ↓
Apply a safe correction or escalate an external fault
  ↓
Verify
  ↓
Retest
  ↓
Document
```



# Lessons Learned

This lab demonstrated that HTTPS troubleshooting is not a single test.

A successful HTTPS connection requires several stages to work:

```text
DNS
→ TCP
→ TLS
→ Certificate Validation
→ HTTP
→ Application
```

The investigation also demonstrated that HTTP status codes provide useful evidence about where to investigate next.

A `301` response demonstrated successful HTTP communication with a redirect.

A `400` response demonstrated that the HTTP service received a request it considered invalid.

A `503` response demonstrated a service availability condition that required comparison against other endpoints and independent services before identifying the fault domain.

Most importantly, the lab reinforced the principle:

> **Do not change a component until evidence indicates that component is responsible for the failure.**


# Conclusion

This lab provided practical experience investigating HTTP and HTTPS communication using `nc` and `curl`.

The investigation progressed from TCP connectivity through TLS, certificate validation, HTTP/2 negotiation, HTTP status-code interpretation, and service fault isolation.

The practical exercises demonstrated how a Network Engineer can move from a reported symptom to evidence-based fault isolation rather than making assumptions about the cause.

The lab also introduced a complete troubleshooting methodology:

