#!/usr/bin/env bash

# Apt
apt-get update

# Python
apt-get install -y python-dev
apt-get install -y python-setuptools
easy_install pip

# install python requirements
sudo -H pip install -r /vagrant/requirements.txt
