"""WSGI file that allows apache to load it."""

import sys

# Set up the environment path and application path. (For CS Server.)
python_path = "/home/weiqi/miniconda3/lib/python3.6/site-packages"
application_path = "/home/weiqi/www/LilyPadz"

# Append important paths.
sys.path.append(python_path)
sys.path.insert(0, application_path)

from application import application
