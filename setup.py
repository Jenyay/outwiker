# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='outwiker',
    version='3.0.0',
    description='A cross-platform software for keeping your notes in a tree',
    author='Eugene Ilin (aka Jenyay)',
    author_email='jenyay.ilin@gmail.com',
    url='https://jenyay.net/Outwiker/English',
    package_dir={'': 'src'},
    packages=find_packages(
        'src',
        exclude=["profiles"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Natural Language :: Ukrainian',
        'Natural Language :: Swedish',
        'Natural Language :: German',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: Office/Business',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: Markup',
    ],
    python_requires='>=3.5',
    install_requires=[
        'wxPython==4.0.7.post2',
        'Pillow>=7.0.0',
        'idna>=2.9',
        'pyparsing>=2.4.6',
        'psutil==5.6.6',
        'cyhunspell>=1.3.4',
        'comtypes>=1.1.7;platform_system=="Windows"',
    ],
    project_urls={
        'Documentation': 'https://outwiker.readthedocs.io/',
        'Issue Tracker': 'https://github.com/Jenyay/outwiker/issues',
    },
)
