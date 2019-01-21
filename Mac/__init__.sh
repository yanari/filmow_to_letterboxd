#!/bin/bash
xcode-select --install
sudo easy_install pip
sudo pip install -U pip
sudo pip robobrowser
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
brew install python3
python3 filmowToLetterboxd.py