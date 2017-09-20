#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# remove currently installed version, if any
. "${DIR}/uninstall.sh"

# copy to /etc/bash_completion.d with no file extension
sudo cp -T "${DIR}/cli_plus.sh" "${INSTALL_PATH}"
