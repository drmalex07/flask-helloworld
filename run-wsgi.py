#!/usr/bin/env python

import os
import argparse
import logging
import logging.config

here = os.path.dirname(os.path.realpath(__file__))

argp = argparse.ArgumentParser()
argp.add_argument("-c", "--config", dest='config_file', 
    default=os.path.join(here, 'config.ini'))
argp.add_argument("-e", "--pyenv", dest='pyenv_dir')
args = argp.parse_args()

config_file = args.config_file

# Activate enviroment if needed

if args.pyenv_dir:
    activate_this = os.path.realpath(
        os.path.join(args.pyenv_dir, 'bin/activate_this.py'))
    execfile(activate_this, dict(__file__=activate_this))

# Setup loggers

logging.config.fileConfig(config_file)

# Configure WSGI application

from helloworld import config, config_from_file

config_from_file(config_file)

# Load and serve WSGI application

from helloworld.wsgi_app import app

# Serve

server_config = config['server']

app.run(
    debug = bool(config.get('debug', False)),
    host = server_config.get('host', '127.0.0.1'),
    port = int(server_config.get('port', 5000)))
