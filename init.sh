#!/bin/bash
sudo apt-get update
sudo apt-get install python3.7
sudo pip install -U pip
sudo pip install -r requirements.txt
python3.7 parser_filmow.py