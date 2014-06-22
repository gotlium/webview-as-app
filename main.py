import sys
import argparse
from PyQt4 import QtGui, QtCore, QtWebKit


class MainWindow(QtGui.QWidget):
    def __init__(self, app):
        QtGui.QWidget.__init__(self)

        args = self.getArgs()

        self.setWindowTitle(args.name)

        app.setApplicationName(args.name)
        app.setWindowIcon(QtGui.QIcon(args.icon))

        self.showWebView(args.url)

    def getArgs(self):
        parser = argparse.ArgumentParser(prog=sys.argv[0])
        parser.add_argument('-u', '--url', help='url for view')
        parser.add_argument('-i', '--icon', help='app icon')
        parser.add_argument('-n', '--name', help='app name')

        return parser.parse_args(sys.argv[1:])

    def showWebView(self, url):
        webView = QtWebKit.QWebView()
        
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(webView)
        layout.setContentsMargins(0, 0, 0, 0)
        
        webView.load(QtCore.QUrl(url))


if __name__ == '__main__':
    app = QtGui.QApplication([])
    main = MainWindow(app)
    main.show()
    sys.exit(app.exec_())
