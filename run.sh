#!/bin/bash

cd "$(dirname "$0")"
git pull origin master
python main.py
git push origin master