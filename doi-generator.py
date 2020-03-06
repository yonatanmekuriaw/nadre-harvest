#!/usr/bin/env python

# A simple python script that create a DOI based on system timestamp.

import cgi,time

doi_prefix='10.20372'
doi =  "%s/nadre/%s" % (doi_prefix,time.time())
print( doi)