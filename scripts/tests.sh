#!/bin/sh
set -e
export TESTRUN_MARKER=True
TEST="bin/python -m cone.fileupload.tests"

clear

if [ -x "$(which python)" ]; then
    ./py2/$TEST
fi

echo ""

if [ -x "$(which python3)" ]; then
    ./py3/$TEST
fi
