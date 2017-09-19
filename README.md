# Dynamic CLI

## Setup

This project is setup to use Vagrant as a development environment.  Run the following commands to get running:

* Provision and start the VM by running `vagrant up`
* Once this has finished, SSH in by running `vagrant ssh`
* Enter the project folder by running `cd /vagrant/project`
* Start the API server running `python api.py`

This will start the Flask development server on http://0.0.0.0:5123.  On the host, navigate to http://localhost:15123 to view the interactive swagger API viewer.

## API

A full JSON representation of the sample API definition can be found at http://localhost:15123/swagger.json

## Usage

To install the autocomplete module, run `./install.sh`. Then, either exit the vagrant SSH session and login again, run `bash --login`, or source the autocomplete file with `. /etc/bash_completion.d/cli_plus`.

Bash autocomplete requires a program name, so for demonstration purposes this is hardcoded to `./autocomplete.py` which must be run from within `/vagrant/project`.

From within the `/vagrant/project` directory, start typing a command starting with `./autocomplete.py` and the program will provide autocomplete suggestions using `[TAB]` as you would expect.  Running the program will take the given input and call the REST method it represents, printing output to the terminal.

## TODO

* better handle scenario where first token isn't a CRUD
* entering a wildcard with a value like {id} seems to make further autocomplete not process
* param names/values with spaces: handle these or not?  Use quotes?
