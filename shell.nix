{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312Full
    autoconf
    automake
    libtool
    gnum4
    gcc
    gnumake
    dpkg
    freeglut
    libGL
    libGLU
    stdenv
    gcc
    python312.pkgs.setuptools
    python312.pkgs.wheel
    freeglut
    mesa
    gtk3
    libjpeg
    libtiff
    libnotify
    libpng
    SDL2
    xorg.libSM
    libtiff
    webkitgtk_4_1
    xorg.libXtst
    pkg-config
    zlib
    gspell
    wxGTK32
    python312Packages.wxpython
  ];
}
