#!/bin/bash

# remove currently installed version, if any
. ./uninstall.sh

# copy to /etc/bash_completion.d with no file extension
sudo cp -T ./cli_plus.sh "${INSTALL_PATH}"
