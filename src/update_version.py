#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

fname = "version.txt"
version = "1.0.0"
status = "dev"

p = subprocess.Popen(["bzr", "revno"], stdout=subprocess.PIPE)
stdout, stderr = p.communicate()

try:
	revision = int(stdout)
except ValueError, e:
	print e
	exit(1)

result = "%s\n%d\n%s\n" % (version, revision + 1, status)
print result

with open (fname, "w") as fp:
	fp.write (result)
