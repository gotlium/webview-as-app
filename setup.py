from setuptools import setup
from glob import glob

APP = ['main.py']
DATA_FILES = [
    ('images', glob('images/*.icns')),
]

OPTIONS = {
    'argv_inject': [
        '-u', 'https://www.google.com/',
        '-n', 'Google Search',
        '-i', 'images/app_icon.icns'
    ],
    'includes': ['sip', 'PyQt4.QtGui', 'PyQt4.QtCore', 'PyQt4.QtWebKit'],
    'semi_standalone': 'False',
    "iconfile": 'images/app_icon.icns',
}

setup(
    name="WebView",
    version="1.0",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=[
        'py2app==0.7.3',
    ],
)
