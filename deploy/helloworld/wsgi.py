#!/usr/bin/env python

import os
import logging.config

config_file = os.path.realpath(os.environ['CONFIG_FILE'])

logging.config.fileConfig(config_file)

from paste.deploy import loadapp
application = loadapp('config:%s' %(config_file))
