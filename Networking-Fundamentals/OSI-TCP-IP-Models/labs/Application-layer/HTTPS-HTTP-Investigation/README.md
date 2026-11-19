




Test 1 — TCP Connectivity

Command:
nc -vz google.com 443

Purpose:
Determine whether a TCP connection can be established with
the destination HTTPS service on port 443.

Result:
Connection succeeded.

Diagnosis:
TCP connectivity to port 443 is functioning.

Limitation:
A successful TCP connection does not prove that TLS,
HTTPS, HTTP, authentication, authorization, or the
application itself is functioning.

## Test 2 — HTTPS/TLS and HTTP Investigation

### Command

```bash
curl -v https://google.com
```

### Purpose

Investigate the complete HTTPS communication process and determine whether the following stages are functioning:

* DNS resolution
* TCP connectivity
* TLS handshake
* TLS certificate validation
* HTTP/2 negotiation
* HTTP request transmission
* HTTP response

The purpose is to identify where communication would stop if an HTTPS connection failed.

### Observed Result

The `curl -v` output demonstrated successful completion of the major stages of the HTTPS connection.

#### 1. DNS Resolution

```text
Host google.com:443 was resolved.
IPv4: 142.251.37.142
```

**Interpretation:**

The hostname `google.com` was successfully resolved to an IPv4 address.

**Diagnosis:**

DNS resolution succeeded.



#### 2. TCP Connection

```text
Connected to google.com (142.251.37.142) port 443
```

**Interpretation:**

The client successfully established a TCP connection with Google's HTTPS service on port 443.

**Diagnosis:**

TCP connectivity to port 443 succeeded.


#### 3. TLS Handshake

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

**Interpretation:**

The client and server successfully completed the TLS handshake and negotiated TLS 1.3.

**Diagnosis:**

TLS negotiation succeeded.



#### 4. TLS Certificate Validation

The server certificate information included:

```text
subject: CN=*.google.com
```

The hostname was successfully matched:

```text
subjectAltName: host "google.com" matched cert's "google.com"
```

The most important validation result was:

```text
SSL certificate verify ok.
```

**Interpretation:**

The certificate was trusted and the hostname matched the certificate's Subject Alternative Name.

**Diagnosis:**

TLS certificate validation succeeded.



#### 5. HTTP/2 Negotiation

The output showed:

```text
ALPN: server accepted h2
using HTTP/2
```

**Interpretation:**

Application Protocol Layer Negotiation (ALPN) successfully negotiated HTTP/2 between the client and server.

**Diagnosis:**

HTTP/2 negotiation succeeded.

---

#### 6. HTTP Request

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

**Interpretation:**

The HTTP request was successfully constructed and transmitted to the server.

**Diagnosis:**

The HTTP request reached the server successfully.

---

#### 7. HTTP Response

The server returned:

```text
HTTP/2 301
```

with:

```text
location: https://www.google.com/
```

**Interpretation:**

HTTP status code `301` means **Moved Permanently**.

The server successfully received and processed the request but instructed the client to use:

```text
https://www.google.com/
```

instead of:

```text
https://google.com/
```

This is a valid HTTP response and does not represent a connectivity failure.

---

# Diagnostic Summary

| Stage                  | Result     | Evidence                            |
| ---------------------- | ---------- | ----------------------------------- |
| DNS resolution         | ✅ Success  | Host resolved                       |
| TCP connectivity       | ✅ Success  | Connected to port 443               |
| TLS handshake          | ✅ Success  | TLS 1.3 established                 |
| Certificate validation | ✅ Success  | `SSL certificate verify ok`         |
| HTTP/2 negotiation     | ✅ Success  | Server accepted `h2`                |
| HTTP request           | ✅ Success  | `GET / HTTP/2` transmitted          |
| HTTP response          | ✅ Success  | `HTTP/2 301`                        |
| Redirect               | ℹ️ Present | `Location: https://www.google.com/` |

---

# Troubleshooting Interpretation

This test demonstrates an important troubleshooting principle:

A successful HTTPS connection does not simply mean that "the website works."

Instead, the communication can be broken into individual stages:

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
```

In this test, every stage completed successfully.

Therefore, there was no evidence of:

* DNS failure
* TCP connectivity failure
* Port 443 failure
* TLS handshake failure
* Certificate validation failure
* HTTP communication failure

The server instead returned a valid `301` redirect.


# Engineering Diagnosis

**Overall result: SUCCESSFUL HTTPS COMMUNICATION**

The client successfully resolved the hostname, established TCP connectivity, completed the TLS 1.3 handshake, validated the server certificate, negotiated HTTP/2, transmitted an HTTP GET request, and received an HTTP response.

The `301` response indicates application-level redirection rather than a network connectivity failure.


# Troubleshooting Value

This test establishes a baseline for later failure investigations.

If a future test fails, the engineer can compare the point at which the communication process stops.

For example:

```text
DNS failure
→ Investigate DNS

TCP connection failure
→ Investigate routing/firewall/port/service

TLS failure
→ Investigate certificates/TLS configuration

HTTP 4xx
→ Investigate client request/authentication/authorization

HTTP 5xx
→ Investigate server/application-side processing
```

The exact cause must still be confirmed with additional evidence rather than assumed from the status code alone.



# Evidence

The successful `curl -v` output should be captured as a screenshot and stored in:

```text
screenshots/
```

Suggested filename:

```text
02-curl-https-verbose.png
```

The screenshot should show the key evidence:

* Host resolution
* TCP connection
* TLS handshake
* Certificate verification
* HTTP/2 negotiation
* HTTP request
* HTTP 301 response

No credentials or authentication tokens were present in the captured output.



# Lessons Learned

This test demonstrated how `curl -v` can be used as an end-to-end Application Layer troubleshooting tool.

Rather than treating HTTPS as a single operation, the output can be analyzed as a sequence of dependent stages.

The test also demonstrated that receiving an HTTP status code means communication progressed beyond the underlying TCP and TLS layers.

A `301` response is therefore evidence that the server was reachable and capable of processing the HTTP request, even though it did not return the final requested page directly.



## Test 3 — HTTP 503 Investigation and Fault Isolation

### Objective

Investigate an unexpected HTTP `503 Service Unavailable` response and determine whether the fault originates from the client network or the remote application/service.



### Test 3A — Initial Request

**Command:**

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

The server returned HTTP status `503 Service Unavailable`.

Although the requested endpoint was intended to produce a `404` response, the expected `404` was not received. Instead, the service returned `503`, indicating that the request reached an HTTP-serving infrastructure layer that was unable to provide the requested service.

The `server: awselb/2.0` header indicates that an AWS Elastic Load Balancer was involved in generating the response.

The exact backend cause cannot be determined from this response alone.



### Test 3B — Compare Another HTTPBin Path

**Command:**

```bash
curl -I https://httpbin.org/
```

### Observed Result

The root path returned the same HTTP response:

```text
HTTP/2 503
server: awselb/2.0
```

### Interpretation

A second, different path also returned `503`.

This reduces the likelihood that the problem was caused solely by the original `/status/404` resource.

The evidence instead suggests a broader availability problem affecting the HTTPBin service or its supporting infrastructure.


### Test 3C — Independent Service Comparison

**Command:**

```bash
curl -I https://example.com
```

### Observed Result

```text
HTTP/2 200
```

### Interpretation

A separate public HTTPS service successfully returned an HTTP `200` response.

This provides an independent comparison and demonstrates that HTTPS communication from the client is functioning normally.



# Fault Isolation

The tests produced the following results:

| Destination              | Result                    |
| ------------------------ | ------------------------- |
| `httpbin.org/status/404` | `503 Service Unavailable` |
| `httpbin.org/`           | `503 Service Unavailable` |
| `example.com/`           | `200 OK`                  |

The evidence indicates:

```text
Client
   ↓
Internet connectivity       ✅
   ↓
HTTPS communication          ✅
   ↓
example.com                  → 200 ✅
   ↓
httpbin.org                  → 503 ⚠️
   ↓
Multiple HTTPBin paths       → 503 ⚠️
```

### Diagnosis

The fault is most likely within the HTTPBin service or its supporting infrastructure rather than the client's basic network connectivity.

The evidence does not justify changing the client's DNS, TCP, TLS, or firewall configuration.



# Remediation

No client-side configuration change was required.

The correct engineering response is to:

1. Document the observed `503` response.
2. Record the affected service and timestamps.
3. Confirm that independent HTTPS services remain reachable.
4. Escalate or report the service-side issue if operating in an enterprise environment.
5. Monitor the service for recovery.
6. Retest the affected service after recovery.

This demonstrates an important troubleshooting principle:

> **Do not modify a functioning component when evidence points to an external fault.**



# Verification

The independent test against `example.com` returned:

```text
HTTP/2 200
```

This verified that the client's HTTPS connectivity remained functional while HTTPBin was returning `503`.

The fault was therefore isolated to the remote service/infrastructure domain with reasonable confidence.



# Troubleshooting Method Applied

```text
Detect
  ↓
HTTPBin returns 503
  ↓
Isolate
  ↓
Test another HTTPBin path
  ↓
Both paths return 503
  ↓
Compare
  ↓
Test independent HTTPS service
  ↓
example.com returns 200
  ↓
Confirm fault domain
  ↓
HTTPBin/service-side infrastructure
  ↓
Remediation
  ↓
No client-side change required
  ↓
Monitor / escalate / retest
```



# Lessons Learned

An HTTP status code should not automatically be treated as proof of a specific root cause.

The `503` response established that the HTTP request reached a service capable of returning an HTTP response, but additional testing was required to determine whether the problem was local or remote.

Testing multiple paths on the affected service and comparing the result against an independent service allowed the fault domain to be narrowed without unnecessarily modifying the client configuration.

The investigation demonstrated the difference between:

* **Finding an error**
* **Identifying the fault domain**
* **Confirming the likely root cause**
* **Applying remediation**
* **Verifying recovery**

In this case, the correct remediation was not to change the client's configuration because the evidence indicated that the client's HTTPS connectivity was functioning.

