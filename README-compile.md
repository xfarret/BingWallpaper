https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/

venv/bin/pip3 install py2app
venv/bin/pip3 install requests
venv/bin/pip3 install PyYaml
venv/bin/pip3 install appscript (not required anymore)


apply corrections qt6:

venv/lib/python3.9/site-packages/py2app/recipes/qt6.py

QLibraryInfo.location(QLibraryInfo.LibrariesPath)
QLibraryInfo.location(QLibraryInfo.PluginsPath)

has to be replaced in recipes/qt6.py by

QLibraryInfo.path(QLibraryInfo.LibraryPath.LibrariesPath)
QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)