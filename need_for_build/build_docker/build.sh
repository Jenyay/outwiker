#!/bin/bash
python3 -m pip install --user pipenv
pipenv run pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython==4.0.1
pipenv update --dev
if [[ $1 =~ ^test.* ]]
then
	xvfb-run pipenv run fab "$@"
else
	pipenv run fab "$@"
fi
