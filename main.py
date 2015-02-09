#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'gotlium'
__version__ = '1.1'

import argparse
import signal
import sys
import os

from PyQt5 import QtCore, QtGui, QtWebKitWidgets, QtWidgets, QtNetwork
from PyQt5.QtWebKit import QWebSettings


class QNetworkCookieJar(QtNetwork.QNetworkCookieJar):
    def __init__(self, cookie_file, parent=None):
        super(QNetworkCookieJar, self).__init__(parent)
        self.cookie_path = os.path.expanduser(cookie_file)

    def saveCookies(self):
        all_cookies = QtNetwork.QNetworkCookieJar.allCookies(self)

        cookie_dir = os.path.dirname(self.cookie_path)
        if not os.path.exists(cookie_dir):
            os.makedirs(cookie_dir)

        with open(self.cookie_path, 'w') as f:
            lines = ''
            for cookie in all_cookies:
                lines += '%s\r\n' % cookie.toRawForm()
            f.writelines(lines)

    def restoreCookies(self):
        if os.path.exists(self.cookie_path):
            with open(self.cookie_path, 'r') as f:
                lines = ''
                for line in f:
                    lines += line
                all_cookies = QtNetwork.QNetworkCookie.parseCookies(lines)
                QtNetwork.QNetworkCookieJar.setAllCookies(self, all_cookies)


class MainWindow(QtWebKitWidgets.QWebView):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.args = self.getArgs()
        self.setPage(QtWebKitWidgets.QWebPage())
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

        if self.args.cookie:
            self.cookie_jar = QNetworkCookieJar(self.args.cookie)
            self.cookie_jar.restoreCookies()

        self.showWebView(self.args.url)

        if self.args.maximize:
            self.showMaximized()

        if self.args.name:
            self.setWindowTitle(self.args.name)
            app.setApplicationName(self.args.name)

        if self.args.icon:
            app.setWindowIcon(QtGui.QIcon(self.args.icon))

        self.showWebView(self.args.url)

    def showWebView(self, url):
        if self.args.cookie:
            self.page().networkAccessManager().setCookieJar(self.cookie_jar)
        self.load(QtCore.QUrl(url))

    def getArgs(self):
        parser = argparse.ArgumentParser(prog=sys.argv[0])
        parser.add_argument('-u', '--url', help='url for view')
        parser.add_argument('-i', '--icon', help='app icon')
        parser.add_argument('-n', '--name', help='app name')
        parser.add_argument('-c', '--cookie', help='cookie file')
        parser.add_argument(
            '-m', '--maximize', help='start as maximized', action="store_true")

        return parser.parse_args(sys.argv[1:])

    def closeEvent(self, event):
        self.cookie_jar.saveCookies()
        event.accept()

    @staticmethod
    def setSettings():
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.AutoLoadImages, True)
        settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebSettings.PluginsEnabled, True)
        settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    main = MainWindow(app)
    main.setSettings()
    main.show()

    if signal.signal(signal.SIGINT, signal.SIG_DFL):
        sys.exit(app.exec_())
    app.exec_()
