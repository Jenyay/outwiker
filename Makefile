outwiker_dir=$(DESTDIR)/usr/share/outwiker/

all:

install:
	mkdir -p $(outwiker_dir)
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/applications
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/16x16/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/22x22/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/24x24/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/32x32/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/64x64/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/128x128/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/256x256/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/apps
	mkdir -p $(DESTDIR)/usr/share/pixmaps/
	cp -r "src/outwiker" $(outwiker_dir)
	cp -r "src/help" $(outwiker_dir)
	cp -r "src/images" $(outwiker_dir)
	cp -r "src/locale" $(outwiker_dir)
	cp -r "src/iconset" $(outwiker_dir)
	cp -r "src/spell" $(outwiker_dir)
	# cp -r "src/plugins" $(outwiker_dir)
	cp -r "src/styles" $(outwiker_dir)
	cp "src/runoutwiker.py" $(outwiker_dir)
	cp "src/version.txt" $(outwiker_dir)
	cp "copyright.txt" $(outwiker_dir)
	cp "README" $(outwiker_dir)
	cp "outwiker" $(DESTDIR)/usr/bin/
	cp "images/outwiker_16.png" $(DESTDIR)/usr/share/icons/hicolor/16x16/apps/outwiker.png
	cp "images/outwiker_22.png" $(DESTDIR)/usr/share/icons/hicolor/22x22/apps/outwiker.png
	cp "images/outwiker_24.png" $(DESTDIR)/usr/share/icons/hicolor/24x24/apps/outwiker.png
	cp "images/outwiker_32.png" $(DESTDIR)/usr/share/icons/hicolor/32x32/apps/outwiker.png
	cp "images/outwiker_48.png" $(DESTDIR)/usr/share/icons/hicolor/48x48/apps/outwiker.png
	cp "images/outwiker_64.png" $(DESTDIR)/usr/share/icons/hicolor/64x64/apps/outwiker.png
	cp "images/outwiker_128.png" $(DESTDIR)/usr/share/icons/hicolor/128x128/apps/outwiker.png
	cp "images/outwiker_256.png" $(DESTDIR)/usr/share/icons/hicolor/256x256/apps/outwiker.png
	cp "images/outwiker.svg" $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/outwiker.svg
	cp "images/outwiker_48.png" $(DESTDIR)/usr/share/pixmaps/outwiker.png
	cp "images/outwiker.xpm" $(DESTDIR)/usr/share/pixmaps/
	cp "outwiker.desktop" $(DESTDIR)/usr/share/applications
	cp -r "man" $(DESTDIR)/usr/share
	cd $(DESTDIR)/usr/share/man/man1; gzip outwiker.1
	cd $(DESTDIR)/usr/share/man/ru/man1; gzip outwiker.1
