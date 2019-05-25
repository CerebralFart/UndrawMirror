#!/bin/bash

cd "$(dirname "$0")"
pip install -r requirements.txt
source ./venv/bin/activate
git pull origin master
python main.py
git push origin master