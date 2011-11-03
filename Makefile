deb:
	cd distrib; sh makedeb.sh

win:
	cd src; python setup_win.py build
	cd distrib\\outwiker_win; 7z a ..\\outwiker_win32_unstable.zip .\\* .\plugins -r -aoa

wintests:
	python src\\setup_tests.py build
