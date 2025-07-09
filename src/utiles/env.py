
import sys

def is_nuitka():
    return any("nuitka" in str(loader).lower() for loader in sys.meta_path)
