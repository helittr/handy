
uv run nuitka --standalone --show-progress --mingw64 --jobs=10 --include-data-dir="src/static/=static/"  --include-data-dir="src/adb/scripts=adb/scripts/" --output-dir=out --main=src/main.py 
