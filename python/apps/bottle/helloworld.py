#!/usr/bin/env python
#!/usr/bin/python3

"""
QUICKSTART: "Hello World"
    https://bottlepy.org/docs/dev/tutorial.html

Usage: ./helloworld.py

Results:
    Visit: http://localhost:8080/hello
"""

from bottle import route, run, template

@route('/')
@route('/hello/<name>')
def hello(name: str='Jedi Master'):
    return template("Hello ,{name}, how are you?", name=name)



# start a built-in development server to run on localhost port 8080
# (serves requests until you hit  Control-c)
run(host='localhost', port=8080, debug=True)