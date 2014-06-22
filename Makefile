build:
	@rm -rf ./build ./dist
	@python setup.py py2app
	@open dist/WebView.app
	@echo "Done"
pack:
	@ln -sf /Applications dist/Applications
	@hdiutil create webview.dmg -volname "webview" -fs HFS+ -srcfolder "dist"
	@echo "Done"
clean:
	@rm -rf ./build ./dist ./*.dmg
	@echo "OK"
