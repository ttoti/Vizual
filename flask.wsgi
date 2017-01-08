#!/usr/bin/python
import sys
import logging
import site
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/CST-205-Proj3/")

site.addsitedir('/var/www/CST-205-Proj3/env/lib/python2.7/site-packages')

import app as application
application.secret_key = 'Add your secret key'
