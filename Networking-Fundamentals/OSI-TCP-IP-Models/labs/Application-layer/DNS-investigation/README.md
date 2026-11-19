# Lab 01 — DNS Investigation

## Objective

Investigate Domain Name System (DNS) resolution from a real macOS network environment and develop the ability to determine whether DNS resolution is functioning correctly.

## Concepts Covered

* DNS
* DNS resolver
* Domain names
* IPv4 address resolution
* DNS records
* A records
* DNS TTL
* DNS queries and responses
* DNS troubleshooting
* DNS failure diagnosis

## Network Environment

| Item             | Details                     |
| ---------------- | --------------------------- |
| Operating System | macOS                       |
| Client           | MacBook Pro                 |
| DNS Resolver     | To be identified during lab |
| Test Domain      | google.com                  |

## Lab Scenario

A user reports that a website cannot be reached.

The first investigation is to determine whether the domain name can be resolved to an IP address.

The troubleshooting process will establish whether the problem is related to:

* DNS resolution
* Network connectivity
* The destination service
* Higher application-layer issues

## Tests

### Test 1 — Basic DNS Resolution

**Command:**

```bash
nslookup google.com
```

**Purpose:**

Determine whether the configured DNS resolver can resolve `google.com` to an IPv4 address.

**Expected evidence:**

* DNS resolver identified
* DNS server address identified
* Requested domain identified
* IPv4 address returned

**Actual Result:**

firewall@joelwilson ~ % nslookup google.com         
Server:		10.101.6.2
Address:	10.101.6.2#53

Non-authoritative answer:
Name:	google.com
Address: 142.251.37.142


Interpretation

The successful response demonstrates that the configured DNS resolver was able to process the query and return an IPv4 address for the requested domain.

Diagnosis

DNS resolution for google.com was functioning successfully at the time of testing.


### Test 2 — Detailed DNS Query

**Command:**

```bash
dig google.com
```

**Purpose:**

Inspect the DNS response in greater detail, including:

* Response status
* Answer section
* Record type
* Returned IPv4 address
* TTL
* Query time
* DNS server used

**Actual Result:**

 firewall@joelwilson ~ % dig google.com


; <<>> DiG 9.10.6 <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40488
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 9


;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;google.com.			IN	A


;; ANSWER SECTION:
google.com.		108	IN	A	142.251.37.142


;; AUTHORITY SECTION:
google.com.		2807	IN	NS	ns3.google.com.
google.com.		2807	IN	NS	ns4.google.com.
google.com.		2807	IN	NS	ns1.google.com.
google.com.		2807	IN	NS	ns2.google.com.


;; ADDITIONAL SECTION:
ns3.google.com.		163330	IN	A	216.239.36.10
ns1.google.com.		163330	IN	A	216.239.32.10
ns4.google.com.		163330	IN	A	216.239.38.10
ns2.google.com.		163330	IN	A	216.239.34.10
ns3.google.com.		163330	IN	AAAA	2001:4860:4802:36::a
ns1.google.com.		163330	IN	AAAA	2001:4860:4802:32::a
ns4.google.com.		163330	IN	AAAA	2001:4860:4802:38::a
ns2.google.com.		163330	IN	AAAA	2001:4860:4802:34::a


;; Query time: 48 msec
;; SERVER: 10.101.6.2#53(10.101.6.2)
;; WHEN: Tue Aug 11 16:24:40 EAT 2026
;; MSG SIZE  rcvd



Interpretation

NOERROR indicates that the DNS server successfully processed the query.

The A record identifies an IPv4 address associated with google.com.

The returned IPv4 address was:

142.251.37.142

The TTL value of 108 seconds represents the remaining cache lifetime of the DNS answer. It does not indicate when the website was last visited.

The NS records identify authoritative name servers associated with the domain.

The query time provides an indication of how quickly the DNS response was received.

Diagnosis

DNS resolution for google.com was functioning successfully at the time of testing.

The evidence establishes that:

DNS query generated       ✅
DNS response received     ✅
Query processed           ✅
A record returned         ✅
IPv4 address returned     ✅

### Test 3 — DNS Resolution Failure

**Command:**

```bash
nslookup this-domain-should-not-exist-123456789.com
```

**Purpose:**

Observe the behavior of DNS when a requested domain cannot be resolved.

**Actual Result:**

server can't find this-domain-should-not-exist-123456789.com: NXDOMAIN

nterpretation

NXDOMAIN means Non-Existent Domain.

The important point is that the DNS resolver responded to the query.

Therefore, this was not evidence that the DNS server itself was unreachable.

The DNS system successfully processed the request but reported that the requested domain does not exist.

**Diagnosis:**

DNS service connectivity was not the problem in this test. The failure was a DNS name-existence/resolution failure because the queried domain does not exist.



## Troubleshooting Methodology

The DNS investigation follows this sequence:

```text
Client generates DNS query
        ↓
DNS resolver identified
        ↓
DNS server reachable
        ↓
DNS query processed
        ↓
DNS response received
        ↓
Record returned
        ↓
Domain resolves to IP address
```

If resolution fails, the investigation will determine whether the problem is related to:

* Incorrect DNS configuration
* DNS server availability
* DNS response failure
* Non-existent domain
* Incorrect DNS record
* Network connectivity to the DNS resolver

## Evidence

Screenshots will be stored in:

```text
screenshots/
```

Evidence will be reviewed for sensitive information before being added to the repository.




*To be completed after all tests have been performed and analyzed.*
Test 4 — DNS Resolver Timeout
Command
dig @192.0.2.1 google.com
Purpose

Demonstrate the difference between a DNS server responding with an error and a DNS server providing no response.

192.0.2.1 is a documentation/test address used here for controlled testing.

Observed Result
;; connection timed out; no servers could be reached
Interpretation

The DNS query received no response from the specified resolver.

This is fundamentally different from NXDOMAIN.

With NXDOMAIN, the DNS server responds and says the domain does not exist.

With a timeout, no usable DNS response was received.

Diagnosis

The result provides evidence of a DNS communication/service availability problem.

Possible areas for investigation include:

DNS server availability
Network connectivity to the resolver
Firewall filtering
Routing
DNS service availability
DNS Troubleshooting Comparison
Result	Meaning	Investigation Direction
NOERROR + A record	Resolution succeeded	Continue to next layer
NXDOMAIN	Domain does not exist	Check domain name/DNS records
Timeout	No DNS response	Investigate DNS server/network/service
No answer	Query processed but requested record may not exist	Check record type/configuration
DNS Troubleshooting Workflow

The investigation follows this general sequence:

Client generates DNS query
        ↓
DNS resolver identified
        ↓
DNS server reachable?
        ↓
DNS query processed?
        ↓
DNS response received?
        ↓
Response status examined
        ↓
Record returned?
        ↓
IP address obtained?

The response determines the next troubleshooting action.

Successful resolution
NOERROR
   ↓
A record
   ↓
IPv4 address
   ↓
DNS functioning
Non-existent domain
NXDOMAIN
   ↓
DNS server responded
   ↓
Domain does not exist
   ↓
Check domain/records
Timeout
TIMEOUT
   ↓
No DNS response
   ↓
Investigate resolver/network/service
DNS Record Types

This section will be completed using the actual outputs from the DNS record investigation.

A Record

Maps a domain/hostname to an IPv4 address.

Example observed during this lab:

google.com → 142.251.37.142
NS Record

Identifies the authoritative name servers responsible for a DNS domain.

MX Record

Identifies the mail servers responsible for receiving email for a domain.

TXT Record

Stores text information associated with a domain. TXT records are commonly used for domain verification and email-security mechanisms.

CNAME Record

Creates an alias from one hostname to another hostname.


Lessons Learned

This lab demonstrated that DNS troubleshooting requires interpreting the actual response rather than simply deciding that "DNS works" or "DNS is broken."

The investigation demonstrated three important conditions:

NOERROR
→ DNS resolution succeeded.

NXDOMAIN
→ DNS responded, but the requested domain does not exist.

TIMEOUT
→ No usable DNS response was received from the specified resolver.

The lab also demonstrated that an A record maps a hostname to an IPv4 address and that DNS responses contain additional information such as TTL and authoritative name-server records.

Conclusion

The DNS investigation demonstrated how to verify DNS resolution, interpret DNS response codes, identify returned records, and distinguish between successful resolution, non-existent domains, and DNS communication failures.

The practical use of nslookup and dig provided evidence-based troubleshooting experience rather than relying solely on theoretical knowledge.

