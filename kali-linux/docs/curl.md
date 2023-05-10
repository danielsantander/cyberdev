
*Table of contents*
- [cURL](#curl)
  - [Resources](#resources)
- [GET Request](#get-request)
- [POST Request](#post-request)
- [PUT Request](#put-request)

# cURL
**cURL** is a computer software project providing a library (libcurl) and command-line tool (curl) for transferring data using various network protocols. The name stands for "Client URL".[wiki](https://en.wikipedia.org/wiki/CURL)

## Resources
[Site](https://curl.se/)
[GitHub](https://github.com/curl/curl)


# GET Request
```shell
curl -X GET '<url_here>' --header "key:value ${ENVIRONMENT_VARIABLE}"
```

# POST Request

```shell
curl -X POST '<url_here>' -H "Content-Type: application/json" -d '{"key1":"value"}'
```

# PUT Request

```shell
curl -X PUT '<url_here>' -H "Content-Type: application/json" -d '{"key1":"value"}'
```
