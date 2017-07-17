# -*- mode: python -*-

block_cipher = None


a = Analysis(['runoutwiker.py'],
             pathex=['src'],
             binaries=[('help', 'help'), ('iconset', 'iconset'), ('images', 'images'), ('locale', 'locale'), ('spell', 'spell'), ('styles', 'styles'), ('plugins', 'plugins')],
             datas=[('versions.xml', '.')],
             hiddenimports=['importlib', 'urllib', 'urllib2', 'outwiker.pages.wiki.wikipanel', 'outwiker.gui.htmlrenderfactory', 'outwiker.gui.controls.popupbutton', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'PIL.ImageFilter', 'PIL.IcoImagePlugin', 'PIL.BmpImagePlugin', 'PIL.TiffImagePlugin', 'enchant', 'htmlentitydefs', 'HTMLParser', 'xml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['Tkinter', 'PyQt4', 'PyQt5', 'unittest', 'distutils', 'setuptools', 'pycparser', 'sqlite3', 'numpy', 'pydoc', 'xmlrpclib', 'test', 'bz2', 'cffi', 'PIL.SunImagePlugin', 'PIL.IptcImagePlugin', 'PIL.McIdasImagePlugin', 'PIL.DdsImagePlugin', 'PIL.FpxImagePlugin', 'PIL.PixarImagePlugin'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='outwiker',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='images/outwiker.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='outwiker')
