!/bin/bash

# stop script on error
set -e

# update system package
sudo apt-get update

# install Python 3.11.6 and pip
sudo apt-get install -y python3.11.6 python3-pip

# verify python version
python3 --version

# install Tkinter
sudo apt-get install -y python3-tk

# install SQLite3 
sudo apt-get install -y sqlite3

# update pip to latest version
python3 -m pip install --upgrade pip

# install Python libraries for application
python3 -m pip install matplotlib numpy beautifulsoup pytest

# verify installation
python3 -c "import tkinter; import sqlite3; import matplotlib; import numpy; import bs4; import pytest; print('All modules installed successfully')"

# run Tkinter
python3 launchGUI.py
