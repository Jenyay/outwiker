#!/bin/sh
python3 -m pip install --user pipenv
pipenv run pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython==4.0.3
pipenv update --dev
pipenv run fab "$@"
