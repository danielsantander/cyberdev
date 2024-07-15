- [Terms](#terms)
  - [CISA](#cisa)
  - [Strict-Transport-Security](#strict-transport-security)

---

# Terms

## CISA
<!-- TODO: continue here -->

## Strict-Transport-Security

The HTTP Strict-Transport-Security response header (HSTS) informs browsers that the site should only be accessed using HTTPS, and that any future attempts to access it using HTTP should automatically be converted to HTTPS.

> Note: This is more secure than simply configuring a HTTP to HTTPS (301) redirect on your server, where the initial HTTP connection is still vulnerable to a man-in-the-middle attack.

SSL/TLS port numbers are the numeric values that specify which port on the web server and web browser will use for the SSL/TLS communication. The default port number for HTTP is 80, while the default port number for HTTPS (HTTP over SSL/TLS) is 443.

Sources:

- [MDN Web Docs:Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
