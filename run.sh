#!/bin/bash
py3="$(python3 --version | sed 's/.* \([0-9]\).\([0-9]\).*/\1/')"

# Make sure python 3 is installed
if [[ $py3 != "3" ]]
then
    echo "Python 3 is required for this app. Please install it first and try again"
    exit 1
fi

# Make sure pip is installed
if [[ -z "$(pip --version)" ]]
then
  echo "pip is required for this app. Please install it first and try again"
  exit 1
fi

# Install and setup Virtualenv
pip install virtualenv
virtualenv env
source env/bin/activate

# Install depedencies and start the app
pip install -r requirement.txt
python3 main.py
