# Dynamic CLI

## What is this Project?

This project is a Dynamic CLI generator designed for use with Flask-RESTPlus, though it should work for any REST API that serves a swagger definition file at http://host:port/swagger.json.  In principle there's no reason that this project couldn't work with any REST service that provides some means of route/method discovery, but for now swagger is all that is supported.

Many projects require both a REST API and a text-based CLI, which generally need to be written separately.  This project is able to parse swagger API definition files and provide a complete, autocomplete-enabled CLI for free with minimal effort.

## Basics

The heart of this project is the `cli_plus` module.  Put this somewhere in `PYTHONPATH` or in your project and you are nearly good to go.  To see how to actually integrate this with a real API, see the samples in `samples/`, along with the `install` and `uninstall` targets in the `Makefile`.

## Sample

The `sample` directory contains a few useful files:

* `api.py` - a sample Flask-RESTPlus API for demonstration purposes.  Once the API server is running, the interactive swagger viewer can be browsed on the host at http://localhost:15123, and the full swagger definition can be found at http://localhost:15123/swagger.json
* `cli_plus.sh` - a sample autocomplete script.  The install script places this in `/etc/bash_completion.d` and then after logging in, bash autocompletion will work for the specified program
* `sample.py` - a sample CLI corresponding to the sample API.  Start typing a command beginning with `./sample.py` from within `/vagrant/sample` and the program will provide autocomplete suggestions using `[TAB]` as you would expect.  Running the program will take the given input and call the REST method it represents against the sample API, printing output to the terminal.
* `install.sh` - install the sample autocomplete program
* `uninstall.sh` - remove the installed sample autocomplete program, if any

## Development Setup

This project is setup to use Vagrant as a development environment.  Run the following commands to get running:

* Provision and start the VM by running `vagrant up`
* Once this has finished, SSH in by running `vagrant ssh`
* Enter the project folder by running `cd /vagrant/sample`
* Start the API server running `python api.py`

This will start the Flask development server on http://0.0.0.0:5123.  On the host, navigate to http://localhost:15123 to view the interactive swagger API viewer.

## Usage

To install the autocomplete module, run `./install.sh`. Then, either exit the vagrant SSH session and login again, run `bash --login`, or source the autocomplete file with `. /etc/bash_completion.d/cli_plus`.

Bash autocomplete requires a program name, so for demonstration purposes this is hardcoded to `./sample.py` which must be run from within `/vagrant/sample`.

## Tests

To run tests, `cd /vagrant/tests` and run `pytest`.  The sample API server will need to be running.

## TODO

* param names/values with spaces: handle these or not?  Use quotes?
* if a param is a file type, send this as a proper file.  Need to store param types as well as names in path tree
* encapsulate swagger-specific code for easier integration of other API types
* tests
* add some level of swagger definition caching
* autocomplete should probably accept a swagger file, rather than create it
