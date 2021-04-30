OUTWIKER_DIR=$(DESTDIR)/usr/share/outwiker
SRC_DIR=src
NFB_LINUX_DIR=need_for_build/linux/
PLUGINS_DIR=plugins
PLUGINS=autorenamer counter datagraph diagrammer export2html externaltools hackpage htmlformatter htmlheads lightbox livejournal markdown pagetypecolor readingmode sessions snippets source spoiler statistics tableofcontents texequation thumbgallery webpage

all:

install:
	mkdir -p $(OUTWIKER_DIR)
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
	cp -r $(SRC_DIR)/help $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/iconset $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/images $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/locale $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/outwiker $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/spell $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/styles $(OUTWIKER_DIR)
	cp -r $(SRC_DIR)/textstyles $(OUTWIKER_DIR)
	mkdir -p $(OUTWIKER_DIR)/plugins
	cp $(SRC_DIR)/runoutwiker.py $(OUTWIKER_DIR)
	cp "copyright.txt" $(OUTWIKER_DIR)
	cp "README" $(OUTWIKER_DIR)
	cp $(NFB_LINUX_DIR)/outwiker $(DESTDIR)/usr/bin/
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
	cp $(NFB_LINUX_DIR)/outwiker.desktop $(DESTDIR)/usr/share/applications
	cp -r $(NFB_LINUX_DIR)/man $(DESTDIR)/usr/share
	cd $(DESTDIR)/usr/share/man/man1; gzip -f outwiker.1
	cd $(DESTDIR)/usr/share/man/ru/man1; gzip -f outwiker.1
	for plugin in $(PLUGINS); do \
		cp -r $(PLUGINS_DIR)/$$plugin/$$plugin $(OUTWIKER_DIR)/plugins; \
	done

uninstall:
	rm -rf $(OUTWIKER_DIR)
	rm -f $(DESTDIR)/usr/bin/outwiker
	rm -f $(DESTDIR)/usr/share/icons/hicolor/16x16/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/22x22/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/24x24/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/32x32/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/48x48/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/64x64/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/128x128/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/256x256/apps/outwiker.png
	rm -f $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/outwiker.svg
	rm -f $(DESTDIR)/usr/share/pixmaps/outwiker.xpm
	rm -f $(DESTDIR)/usr/share/pixmaps/outwiker.png
	rm -f $(DESTDIR)/usr/share/applications/outwiker.desktop
	rm -f $(DESTDIR)/usr/share/man/man1/outwiker.1.gz
	rm -f $(DESTDIR)/usr/share/man/ru/man1/outwiker.1.gz

