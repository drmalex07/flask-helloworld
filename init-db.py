#!/usr/bin/env python

import os
import argparse

here = os.path.dirname(os.path.realpath(__file__))

argp = argparse.ArgumentParser()
argp.add_argument("-c", "--config", dest='config_file', 
    default=os.path.join(here, 'config.ini'))
argp.add_argument("-e", "--pyenv", dest='pyenv_dir')
argp.add_argument("-n", "--name", dest='app_name', default='main')
argp.add_argument("-r", "--recreate", dest='recreate', action='store_true')
argp.add_argument("-v", "--verbose", dest='verbose', action='store_true',
    help='Be verbose (echo queries)')
args = argp.parse_args()

config_file = os.path.realpath(args.config_file)
config_uri = 'config:%s#%s' % (config_file, args.app_name)

# Activate enviroment if needed

if args.pyenv_dir:
    activate_this = os.path.realpath(
        os.path.join(args.pyenv_dir, 'bin/activate_this.py'))
    execfile(activate_this, dict(__file__=activate_this))

# Import project-specific modules

import paste.deploy
import sqlalchemy

import helloworld.model as model

# Load app configuration

config = paste.deploy.appconfig(config_uri)

database_url = config['database.url']

# Create database schema

engine = sqlalchemy.create_engine(database_url, echo=args.verbose)

if args.recreate:
    model.Base.metadata.drop_all(bind=engine)

model.Base.metadata.create_all(bind=engine)
