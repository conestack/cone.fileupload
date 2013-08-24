#!/bin/bash

python setup.py extract_messages

cat src/cone/fileupload/locale/manual.pot >> \
src/cone/fileupload/locale/cone.fileuplaod.pot

python setup.py update_catalog
