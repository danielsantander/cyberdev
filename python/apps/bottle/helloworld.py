#!/usr/bin/env python
#!/usr/bin/python3

"""
QUICKSTART: "Hello World"
    https://bottlepy.org/docs/dev/tutorial.html

Usage: ./helloworld.py

Results:
    Visit: http://localhost:8080/hello
"""

import datetime
import json
import logging
import os
from bottle import request, route, run, template
from pathlib import Path

_TODAY = datetime.datetime.now()
_MONTH = _TODAY.strftime("%B")
_MONTH_NUM = f"{_TODAY.month:02}"
_DAY = f"{_TODAY.day:02}"
_YEAR = _TODAY.strftime("%Y")
_HOUR = f"{_TODAY.hour:02}"
_MINUTE = f"{_TODAY.minute:02}"
_SECOND = f"{_TODAY.second:02}"

DEBUG_MODE: bool = True
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_LEVEL: int = logging.DEBUG if DEBUG_MODE else logging.INFO
LOG_FORMAT_STR = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FORMAT = logging.Formatter(LOG_FORMAT_STR)

# logger
log_format = logging.Formatter(LOG_FORMAT_STR)
logger = logging.getLogger("BottleApp")
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)

def write_json_to_file(filepath:Path, data:dict):
    """ Write data to JSON file. """
    if not filepath.exists():
        if not filepath.parent.exists(): filepath.parent.mkdir()
        filepath.touch()
    filepath = filepath if str(filepath.name).endswith('.json') else filepath.parent/f"{filepath.stem}.json"
    with open(filepath.absolute(), "w") as f:
        # json.dump(dict, f, indent=2)  # should work as well
        f.write(json.dumps(data, indent=2))
    return


@route('/')
@route('/hello')
@route('/hello/')
@route('/hello/<name>/')
@route('/hello/<name>')
def hello(name: str='Jedi Master'):
    headers = dict(request.headers)
    logger.info(f"Endpoint reached, headers:\n{headers}")
    output_file = Path(CUR_DIR) / 'sample_data' / f'{_YEAR}{_MONTH_NUM}{_DAY}{_HOUR}{_MINUTE}{_SECOND}--headers.json'
    write_json_to_file(output_file, headers)
    return f"Hello, {name.capitalize()}, how are you?"

# start a built-in development server to run on localhost port 8080
# (serves requests until you hit  Control-c)
run(host='localhost', port=8080, debug=True)