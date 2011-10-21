deb:
	cd ../distrib; sh makedeb.sh

win:
	python setup_win.py build
	7z a -r -tzip ..\\distrib\\outwiker_win32_unstable.zip ..\\distrib\\outwiker_win\\*.* ..\\distrib\\outwiker_win\\plugins

wintests:
	python setup_tests.py build
