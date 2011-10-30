deb:
	cd distrib; sh makedeb.sh

win:
	python src\\setup_win.py build
	7z a -r -tzip distrib\\outwiker_win32_unstable.zip distrib\\outwiker_win\\*.* distrib\\outwiker_win\\plugins

wintests:
	python src\\setup_tests.py build
