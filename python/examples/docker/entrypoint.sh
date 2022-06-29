#!/bin/sh

test() {
    echo 'Starting tests...'
    # todo add testing
    echo 'Testing complete.'
}

test

cd /app/src/

python3  -m flask run --host=0.0.0.0
