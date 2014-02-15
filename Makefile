dirname=outwiker-1.8.0
origname=outwiker_1.8.0.orig.tar
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
	# cp -r "src/plugins" $(outwiker_dir)
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
	cd src && python setup_win.py build
	cd build\\outwiker_win && 7z a ..\outwiker_win32_unstable.zip .\* .\plugins -r -aoa
	cd build\\outwiker_win && 7z a ..\outwiker_win32_unstable.7z .\* .\plugins -r -aoa
	iscc outwiker_setup.iss

plugin:
	rm -f build/plugins/outwiker-plugins-all.zip
	rm -f build/plugins/source.zip
	cd plugins/source; 7z a -r -aoa -xr!*.pyc ../../build/plugins/source.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/style.zip
	cd plugins/style; 7z a -r -aoa -xr!*.pyc ../../build/plugins/style.zip ./* ; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/export2html.zip
	cd plugins/export2html; 7z a -r -aoa -xr!*.pyc ../../build/plugins/export2html.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/spoiler.zip
	cd plugins/spoiler; 7z a -r -aoa -xr!*.pyc ../../build/plugins/spoiler.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/livejournal.zip
	cd plugins/livejournal; 7z a -r -aoa -xr!*.pyc ../../build/plugins/livejournal.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/lightbox.zip
	cd plugins/lightbox; 7z a -r -aoa -xr!*.pyc ../../build/plugins/lightbox.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/thumbgallery.zip
	cd plugins/thumbgallery; 7z a -r -aoa -xr!*.pyc ../../build/plugins/thumbgallery.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/externaltools.zip
	cd plugins/externaltools; 7z a -r -aoa -xr!*.pyc ../../build/plugins/externaltools.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	rm -f build/plugins/statistics.zip
	cd plugins/statistics; 7z a -r -aoa -xr!*.pyc ../../build/plugins/statistics.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*
	cd plugins/updatenotifier; 7z a -r -aoa -xr!*.pyc ../../build/plugins/updatenotifier.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*

wintests:
	cd src && python setup_tests.py build

source: clean
	mkdir -p build/$(dirname)
	rsync -avz --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe * --exclude=src/.ropeproject --exclude=src/test --exclude=src/setup_win.py --exclude=src/setup_tests.py --exclude=src/profile.py --exclude=src/tests.py --exclude=src/Microsoft.VC90.CRT.manifest --exclude=src/profiles --exclude=src/tools --exclude=doc --exclude=plugins --exclude=profiles --exclude=test --exclude=_update_version_bzr.py --exclude=outwiker_setup.iss --exclude=updateversion --exclude=updateversion.py build/$(dirname)/

orig: source
	cd build; tar -cvf $(origname) $(dirname)
	gzip -f build/$(origname)



