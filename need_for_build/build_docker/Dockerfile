FROM ubuntu:xenial

LABEL maintainer="Eugene Ilin <jenyay.ilin@gmail.com>"

RUN apt-get -y update && apt-get -y install python3-pip python3-dev debhelper devscripts debhelper devscripts p7zip-full libssl-dev dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libnotify-dev freeglut3 ibus-gtk3 xvfb wget fuse libhunspell-dev ruby libgcrypt20-dev libwebp-dev libxslt1-dev libsecret-1-dev libtasn1-6-dev libenchant-dev libhyphen-dev libjpeg-dev libsoup2.4-dev libxkbcommon-dev libnghttp2-14 libpixman-1-dev libsqlite3-dev libgl1-mesa-dev freeglut3-dev libgirepository1.0-dev libgtk-3-dev libgtk2.0-dev libnotify-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libc6 libstdc++6 libgl1 libgles2 geoclue-2.0 gperf gobject-introspection software-properties-common

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 HOME=/home/user WEBKITGTK_NAME=webkitgtk-2.24.1
ENV PROJECT_HOME=$HOME/project CONFIG_PATH=$HOME/.config
ENV PATH=$PATH:$HOME/.local/bin

RUN add-apt-repository --yes ppa:ubuntu-toolchain-r/test && apt-get update && apt-get -y install gcc-6 g++-6 cmake
RUN cd /tmp && wget https://www.webkitgtk.org/releases/$WEBKITGTK_NAME.tar.xz && tar -xJf $WEBKITGTK_NAME.tar.xz
RUN cd /tmp/$WEBKITGTK_NAME && cmake -DCMAKE_INSTALL_PREFIX=/ -DCMAKE_BUILD_TYPE=Release -DPORT=GTK -DENABLE_WEB_CRYPTO=0 -DUSE_OPENJPEG=0 -DUSE_WOFF2=0 -DUSE_GSTREAMER_GL=0 -DENABLE_MEDIA_SOURCE=0 -DLIBEXEC_INSTALL_DIR=/usr/libexec/webkit2gtk-4.0 -DCMAKE_C_COMPILER=gcc-6 -DCMAKE_CXX_COMPILER=g++-6 . && make -j$(nproc) && make install

RUN mkdir -p $HOME && mkdir -p $CONFIG_PATH && mkdir -p $PROJECT_HOME

RUN groupadd -r user && useradd -r -g user -d $HOME -s /sbin/nologin -c "Docker image user" user
RUN chown -R user:user $HOME && chmod -R 777 $HOME

COPY build.sh /

USER user
WORKDIR $PROJECT_HOME

ENTRYPOINT ["/bin/bash", "/build.sh"]
CMD ["linux_binary", "linux_appimage", "deb_binary", "plugins"]
