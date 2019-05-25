#!/bin/bash

cd "$(dirname "$0")"
git pull origin master
python3 main.py
git push origin master
