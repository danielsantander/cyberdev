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

def get_dates():
    now = datetime.datetime.now()
    year_num = now.strftime("%Y")
    month_num = f"{now.month:02}"
    day_num = f"{now.day:02}"
    hour = f"{now.hour:02}"
    minute = f"{now.minute:02}"
    second = f"{now.second:02}"
    return year_num, month_num, day_num, hour, minute, second

def write_json_to_file(filepath:Path, data:dict):
    """ Write data to JSON file. """
    if not filepath.parent.exists(): filepath.parent.mkdir()
    filepath = filepath if str(filepath.name).endswith('.json') else filepath.parent/f"{filepath.stem}.json"
    if not filepath.exists(): filepath.touch()
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
    year_num, month_num, day_num, hour, minute, second = get_dates()
    headers = dict(request.headers)
    logger.info(f"Endpoint reached, headers: {headers}")
    output_file = Path(CUR_DIR) / 'sample_data' / f'{year_num}{month_num}{day_num}{hour}{minute}{second}--headers.json'
    write_json_to_file(output_file, headers)
    return f"Hello, {name.capitalize()}, how are you?"

# start a built-in development server to run on localhost port 8080
# (serves requests until you hit  Control-c)
run(host='localhost', port=8080, debug=True)