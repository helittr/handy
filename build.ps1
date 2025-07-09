
uv run nuitka --standalone --show-progress --mingw64 --jobs=8 --include-data-dir="../handy/dist/=static/"  --include-data-dir="src/adb/scripts=adb/scripts/" --output-dir=out --windows-icon-from-ico=./src/static/h.ico  --windows-console-mode=disable  --main=src/main.py 
