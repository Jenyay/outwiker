#!/bin/bash

git clone https://github.com/wxWidgets/Phoenix
cd Phoenix
git checkout wxPython-$WX_VERSION
git submodule init
git submodule update
python3 build.py dox etg --nodoc sip build bdist_wheel
cp -f dist/* $BUILD
