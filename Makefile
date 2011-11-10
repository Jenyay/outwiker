deb:
	cd distrib; sh makedeb.sh

win:
	cd src; python setup_win.py build
	cd distrib\\outwiker_win; 7z a ..\\outwiker_win32_unstable.zip .\\* .\plugins -r -aoa

plugin:
	rm -f distrib/source.zip
	cd plugins/source; 7z a -r -aoa -xr!*.pyc ../../distrib/source.zip ./* 
	rm -f distrib/style.zip
	cd plugins/style; 7z a -r -aoa -xr!*.pyc ../../distrib/style.zip ./* 
	rm -f distrib/testdebug.zip
	cd plugins/testdebug; 7z a -r -aoa -xr!*.pyc ../../distrib/testdebug.zip ./* 
	rm -f distrib/testcounter.zip
	cd plugins/testcounter; 7z a -r -aoa -xr!*.pyc ../../distrib/testcounter.zip ./* 

wintests:
	python src\\setup_tests.py build
