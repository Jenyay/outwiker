FROM ubuntu:xenial

LABEL maintainer="Eugene Ilin <jenyay.ilin@gmail.com>"

RUN apt-get -y update && apt-get -y install python3-pip python3-dev debhelper devscripts debhelper devscripts p7zip-full libssl-dev dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libnotify-dev freeglut3 ibus-gtk3 xvfb wget fuse
# RUN apt-get -y install libwebkit2gtk-4.0
RUN apt-get -y install libwebkitgtk-3.0

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 HOME=/home/user
ENV PROJECT_HOME=$HOME/project CONFIG_PATH=$HOME/.config
ENV PATH=$PATH:$HOME/.local/bin

RUN mkdir -p $HOME && mkdir -p $CONFIG_PATH && mkdir -p $PROJECT_HOME

RUN groupadd -r user && useradd -r -g user -d $HOME -s /sbin/nologin -c "Docker image user" user
RUN chown -R user:user $HOME && chmod -R 777 $HOME

COPY build.sh /

USER user
WORKDIR $PROJECT_HOME

ENTRYPOINT ["/bin/bash", "/build.sh"]
CMD ["linux_binary", "linux_appimage", "deb_binary", "plugins"]
