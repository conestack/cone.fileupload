#!/bin/sh
export TESTRUN_MARKER=True

./$1/bin/coverage run --source src/cone/fileupload -m cone.fileupload.tests
./$1/bin/coverage report
./$1/bin/coverage html
