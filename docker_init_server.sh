#!/bin/sh

python -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
python setup.py develop

ifconfig |grep "inet addr"
bluserver --address=0.0.0.0 --verbose
