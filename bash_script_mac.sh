#!/bin/bash

# stop script on error
set -e

# install Homebrew if not installed 
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# install pyenv to manage Python versions
brew install pyenv


# check if Python 3.11.6 is installed
if pyenv versions | grep -q "3.11.6"; then
    echo "Python 3.11.6 is already installed."
else
    echo "Installing Python 3.11.6..."
    pyenv install 3.11.6
fi

# set python version
pyenv global 3.11.6

# verify Python version
python3 --version


# install python libraries
pip install matplotlib numpy beautifulsoup4 pytest

# install SQLite3 with brew 
brew install sqlite3 

# verify installations
python3 -c "import tkinter; import sqlite3; import matplotlib; import numpy; import bs4; import pytest; print('All packages installed successfully')"

python3 launchGUI.py
