#!/usr/bin/env bash

# Apt
apt-get update
apt-get install -y make

# Python
apt-get install -y python-dev
apt-get install -y python-setuptools
easy_install pip

# install python requirements
sudo -H pip install -r /vagrant/requirements.txt

# install sample autocompletion
pushd /vagrant
    make install
popd
