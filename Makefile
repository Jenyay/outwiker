dirname=outwiker-1.7.0
origname=outwiker_1.7.0.orig.tar
outwiker_dir=$(DESTDIR)/usr/share/outwiker/

all:

clean:
	rm -rf build/$(dirname)

install:
	mkdir -p $(outwiker_dir)
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/applications
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/16x16/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/32x32/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/64x64/apps
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/apps
	mkdir -p $(DESTDIR)/usr/share/pixmaps/
	cp -r "src/outwiker" $(outwiker_dir)
	cp -r "src/help" $(outwiker_dir)
	cp -r "src/images" $(outwiker_dir)
	cp -r "src/locale" $(outwiker_dir)
	cp -r "src/plugins" $(outwiker_dir)
	cp -r "src/styles" $(outwiker_dir)
	cp "src/runoutwiker.py" $(outwiker_dir)
	cp "src/version.txt" $(outwiker_dir)
	cp "copyright" $(outwiker_dir)
	cp "README" $(outwiker_dir)
	cp "outwiker" $(DESTDIR)/usr/bin/
	cp "images/outwiker_16.png" $(DESTDIR)/usr/share/icons/hicolor/16x16/apps/outwiker.png
	cp "images/outwiker_32.png" $(DESTDIR)/usr/share/icons/hicolor/32x32/apps/outwiker.png
	cp "images/outwiker_48.png" $(DESTDIR)/usr/share/icons/hicolor/48x48/apps/outwiker.png
	cp "images/outwiker_64.png" $(DESTDIR)/usr/share/icons/hicolor/64x64/apps/outwiker.png
	cp "images/outwiker.svg" $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/outwiker.svg
	cp "images/outwiker.xpm" $(DESTDIR)/usr/share/pixmaps/
	cp "outwiker.desktop" $(DESTDIR)/usr/share/applications

debsource: source
	cd build/$(dirname)/debian; debuild -S --source-option=--include-binaries --source-option=--auto-commit

debsourceinclude: source
	cd build/$(dirname)/debian; debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit

deb: source
	cd build/$(dirname)/debian; debuild --source-option=--include-binaries --source-option=--auto-commit

win:
	cd src; python setup_win.py build
	cd build\\outwiker_win; 7z a ..\\outwiker_win32_unstable.zip .\\* .\plugins -r -aoa

plugin:
	rm -f build/plugins/source.zip
	cd plugins/source; 7z a -r -aoa -xr!*.pyc ../../build/plugins/source.zip ./* 
	rm -f build/plugins/style.zip
	cd plugins/style; 7z a -r -aoa -xr!*.pyc ../../build/plugins/style.zip ./* 
	rm -f build/plugins/testdebug.zip
	cd plugins/testdebug; 7z a -r -aoa -xr!*.pyc ../../build/plugins/testdebug.zip ./* 
	rm -f build/plugins/testcounter.zip
	cd plugins/testcounter; 7z a -r -aoa -xr!*.pyc ../../build/plugins/testcounter.zip ./* 
	rm -f build/plugins/export2html.zip
	cd plugins/export2html; 7z a -r -aoa -xr!*.pyc ../../build/plugins/export2html.zip ./*
	rm -f build/plugins/spoiler.zip
	cd plugins/spoiler; 7z a -r -aoa -xr!*.pyc ../../build/plugins/spoiler.zip ./*
	rm -f build/plugins/livejournal.zip
	cd plugins/livejournal; 7z a -r -aoa -xr!*.pyc ../../build/plugins/livejournal.zip ./*
	rm -f build/plugins/lightbox.zip
	cd plugins/lightbox; 7z a -r -aoa -xr!*.pyc ../../build/plugins/lightbox.zip ./*
	rm -f build/plugins/thumbgallery.zip
	cd plugins/thumbgallery; 7z a -r -aoa -xr!*.pyc ../../build/plugins/thumbgallery.zip ./*
	rm -f build/plugins/externaltools.zip
	cd plugins/externaltools; 7z a -r -aoa -xr!*.pyc ../../build/plugins/externaltools.zip ./*

wintests:
	python src\\setup_tests.py build

source: clean
	mkdir -p build/$(dirname)
	rsync -avz --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe * --exclude=src/.ropeproject build/$(dirname)/

orig: source
	cd build; tar -cvf $(origname) $(dirname)
	gzip -f build/$(origname)



