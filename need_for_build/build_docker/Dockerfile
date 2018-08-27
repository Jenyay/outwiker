FROM ubuntu:xenial

LABEL maintainer="jenyay.ilin@gmail.com"

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN apt-get -y update && apt-get -y install python3-pip python3-dev debhelper devscripts debhelper devscripts p7zip-full libssl-dev dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libnotify-dev freeglut3 ibus-gtk3 xvfb wget fuse
RUN apt-get -y install libwebkit2gtk-4.0
RUN python3 -m pip install pipenv

WORKDIR /project
RUN pipenv run pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython==4.0.3
CMD pipenv update --dev && pipenv run fab linux_binary linux_appimage deb_binary plugins
