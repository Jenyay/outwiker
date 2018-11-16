FROM ubuntu:bionic

LABEL maintainer="Eugene Ilin <jenyay.ilin@gmail.com>"

RUN apt-get -y update && apt-get -y install python python3-pip python3-dev libssl-dev dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl2-dev libgstreamer-plugins-base1.0-dev libnotify-dev freeglut3 freeglut3-dev libsm-dev libgtk-3-dev ibus-gtk3 xvfb wget fuse libhunspell-dev git

# RUN apt-get -y install libwebkit2gtk-4.0 libwebkit2gtk-4.0-dev
RUN apt-get -y install libwebkitgtk-3.0 libwebkitgtk-3.0-dev
RUN python3 -m pip install wheel requests

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 HOME=/home/user BUILD=/home/user/build
ENV PATH=$PATH:$HOME/.local/bin

RUN mkdir -p $HOME

RUN groupadd -r user && useradd -r -g user -d $HOME -s /sbin/nologin -c "Docker image user" user
RUN chown -R user:user $HOME && chmod -R 777 $HOME

COPY build.sh /

USER user
WORKDIR $HOME
RUN mkdir -p $BUILD

ENTRYPOINT ["/bin/bash"]
CMD ["/build.sh"]
