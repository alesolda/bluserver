#!/bin/sh

python -m venv ./venv
. venv/bin/activate
pip install -r requirements_dev.txt
python setup.py develop
pytest --cov=bluserver
