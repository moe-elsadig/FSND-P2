#!/usr/bin/python
import sys

sys.path.insert(0,"/var/www/catalogue_web/")

from __init__ import app as application

application.secret_key = 'super_secret_key'
