#!/usr/bin/env python

import os
import argparse
import logging
import logging.config
from paste.deploy import loadapp, loadserver

here = os.path.dirname(os.path.realpath(__file__))

argp = argparse.ArgumentParser()
argp.add_argument("-c", "--config", dest='config_file', 
    default=os.path.join(here, 'config.ini'))
argp.add_argument("-e", "--pyenv", dest='pyenv_dir')
args = argp.parse_args()

config_file = args.config_file
config_uri = 'config:%s' %(config_file)

# Activate enviroment if needed

if args.pyenv_dir:
    activate_this = os.path.realpath(
        os.path.join(args.pyenv_dir, 'bin/activate_this.py'))
    execfile(activate_this, dict(__file__=activate_this))

# Setup loggers

logging.config.fileConfig(config_file)

# Load application

app = loadapp(config_uri);

# Load server

server = loadserver(config_uri)

# Serve 

server(app)
