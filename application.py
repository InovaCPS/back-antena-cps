#!/usr/bin/env python3
#
#   This script will run the main application file in debug mode.
#
#   author: Michael Gruber
#
#   Adapted by Lucas Nadalete

from sys import path
import os.path
path.append('src/main/python/')

from helper.config_helper import ConfigHelper
from webapp import application, APP_RESOURCE

# Load server configuration
helper = ConfigHelper(APP_RESOURCE)
chost = helper.get_property_by_section('server', 'inova.host')
cport = int(helper.get_property_by_section('server', 'inova.port'))
cdebug = bool(helper.get_property_by_section('server', 'inova.debug'))

# Start Web Server for all hosts, ssl_context=('cert.pem', 'key.pem')

if __name__ == "__main__":
    application.run(host=chost, debug=cdebug, port=cport)