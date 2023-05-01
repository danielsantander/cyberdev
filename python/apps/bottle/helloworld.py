#!/usr/bin/env python
#!/usr/bin/python3

"""
QUICKSTART: "Hello World"
    https://bottlepy.org/docs/dev/tutorial.html

Usage: ./helloworld.py

Results:
    Visit: http://localhost:8080/hello
"""

from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8080, debug=True)