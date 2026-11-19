# Lab 03 — Authentication Investigation

## Objective

Investigate HTTP authentication using a controlled public test service and demonstrate how an authentication failure can be identified, remediated, and verified.

The lab focuses on distinguishing **authentication** from other Application Layer problems and applies the troubleshooting workflow:

```text
Detect → Isolate → Confirm → Remediate → Verify → Document
```



# Concepts Covered

* HTTP authentication
* HTTP `401 Unauthorized`
* HTTP `Authorization` header
* HTTP Basic Authentication
* `curl -u`
* Username and password credentials
* Authentication failure
* Authentication remediation
* Authentication verification
* Authentication vs authorization
* Evidence-based troubleshooting



# Security Considerations

This lab uses a controlled public testing service and intentionally provided dummy credentials.

The credentials used were:

```text
Username: user
Password: passwd
```

These are **not personal credentials**.

Real passwords, API keys, VPN credentials, session cookies, or authentication tokens should never be included in screenshots or public documentation.

For real authentication testing, avoid placing passwords directly in shell commands where possible.



# Test 1 — Unauthenticated Request

## Command

```bash
curl -I https://httpbingo.org/basic-auth/user/passwd
```

## Purpose

Determine how the server responds when a protected resource is requested without authentication credentials.



## Observed Result

```text
HTTP/2 401
access-control-allow-credentials: true
access-control-allow-origin: *
content-type: application/json; charset=utf-8
www-authenticate: Basic realm="Fake Realm"
date: Wed, 12 Aug 2026 08:33:38 GMT
server: Fly/505080ed8 (2026-08-11)
via: 2 fly.io, 2 fly.io
fly-request-id: 01KZTHP304T5J2
```



## Interpretation

The server returned:

```text
HTTP/2 401
```

`401 Unauthorized` indicates that the requested resource requires authentication and that acceptable authentication credentials were not supplied.

The most important supporting evidence was:

```text
www-authenticate: Basic realm="Fake Realm"
```

This header tells the client which authentication scheme the server expects.

In this case, the server indicated **HTTP Basic Authentication**.



# Authentication Troubleshooting Analysis

The communication can be represented as:

```text
Client
  ↓
DNS                     ✅
  ↓
TCP                     ✅
  ↓
TLS                     ✅
  ↓
HTTP request             ✅
  ↓
Authentication required  ⚠️
  ↓
No credentials
  ↓
401 Unauthorized
```

The evidence indicates that the request successfully reached the HTTP service.

Therefore, this was not treated as:

* DNS failure
* TCP failure
* TLS failure
* HTTPS connectivity failure
* Server unreachable

The investigation was narrowed to the authentication stage.



# Test 2 — Authentication Remediation

## Command

```bash
curl -I -u user:passwd https://httpbingo.org/basic-auth/user/passwd
```

## Purpose

Provide the correct test credentials and determine whether authentication is the cause of the `401` response.



# Understanding `-u`

The `-u` option is an abbreviation for:

```bash
--user
```

The syntax used was:

```text
-u username:password
```

Therefore:

```text
-u user:passwd
```

means:

```text
Username → user
Password → passwd
```

`curl` uses these credentials for HTTP Basic Authentication.

Conceptually:

```text
Username + Password
        ↓
HTTP Basic Authentication
        ↓
Authorization header
        ↓
Server validates credentials
```



# Observed Result

```text
HTTP/2 200
access-control-allow-credentials: true
access-control-allow-origin: *
content-type: application/json; charset=utf-8
date: Wed, 12 Aug 2026 08:35:47 GMT
server: Fly/505080ed8 (2026-08-11)
via: 2 fly.io, 2 fly.io
fly-request-id: 01KZTHT18Y1GXYDQ9KQPBDZYX0-fra
```



# Interpretation

After supplying the correct test credentials, the server returned:

```text
HTTP/2 200
```

This indicates that the authentication requirement was successfully satisfied for the controlled endpoint.

The change from:

```text
401
```

to:

```text
200
```

provides strong evidence that the missing authentication credentials were responsible for the original failure.



# Before and After

## Before Authentication

```text
Request
   ↓
Protected resource
   ↓
No credentials
   ↓
401 Unauthorized ❌
```

## After Authentication

```text
Request
   ↓
Protected resource
   ↓
Correct test credentials
   ↓
Authentication succeeds
   ↓
200 OK ✅
```



# Troubleshooting Cycle

The complete troubleshooting process was:

```text
Detect
  ↓
401 Unauthorized
  ↓
Isolate
  ↓
WWW-Authenticate: Basic
  ↓
Confirm
  ↓
Authentication credentials required
  ↓
Remediate
  ↓
Supply valid test credentials
  ↓
Verify
  ↓
HTTP/2 200
  ↓
Document
```


# Diagnosis

### Initial fault

The protected resource was requested without authentication credentials.

### Evidence

```text
HTTP/2 401
```

and:

```text
WWW-Authenticate: Basic
```

### Remediation

Valid test credentials were supplied using:

```bash
-u user:passwd
```

### Verification

The server returned:

```text
HTTP/2 200
```

### Final conclusion

The investigation demonstrated that the original `401` response was caused by the absence of acceptable authentication credentials.


# Authentication vs Authorization

This lab demonstrates **authentication**, not authorization.

Authentication answers:

> **Who are you?**

Authorization answers:

> **What are you allowed to access?**

The current investigation can therefore be represented as:

```text
Authentication
      ↓
"Who are you?"
      ↓
Credentials supplied
      ↓
Identity accepted
      ↓
200 OK
```

A successfully authenticated user may still be denied access to a resource they are not permitted to use.

That situation will be investigated separately using an HTTP `403 Forbidden` scenario.



# Security Note — Using `curl -u`

The command:

```bash
curl -I -u user:passwd https://httpbingo.org/basic-auth/user/passwd
```

was safe in this lab because the credentials were deliberately created for testing.

However, real passwords should not normally be placed directly in commands because they may be exposed through shell history or other local process information.

For real authentication testing, a safer approach is:

```bash
curl -I -u username https://example.com
```

which allows `curl` to prompt for the password rather than placing it directly in the command.



# Lessons Learned

This lab demonstrated that an HTTP `401` response should not automatically be treated as a general connectivity failure.

The request successfully reached the HTTP service, which explicitly indicated that authentication was required.

The `WWW-Authenticate` response header provided additional evidence about the authentication mechanism.

Supplying the correct test credentials changed the response from:

```text
401 Unauthorized
```

to:

```text
200 OK
```

This provided practical evidence that authentication was the cause of the initial failure.

The lab also reinforced the distinction between:

```text
Authentication → Who are you?

Authorization → What are you allowed to access?
```



# Conclusion

This lab demonstrated practical HTTP authentication troubleshooting using `curl`.

The investigation progressed from an unauthenticated request producing `401 Unauthorized` to supplying valid test credentials and verifying successful authentication through a `200 OK` response.

The exercise demonstrated the complete troubleshooting methodology:


