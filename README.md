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
