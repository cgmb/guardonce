#!/usr/bin/env python

import sys
import os
from os.path import join
from fnmatch import fnmatch
import crules

def printError(error):
	print >> sys.stderr, error

def applyToHeaders(func,directory,exclude):
	for root, dirs, files in os.walk(directory, onerror=printError):
		for fileName in files:
			filePath = join(root,fileName)
			if exclude and fnmatch(filePath, exclude):
				continue
			if crules.isHeaderFile(fileName):
				func(filePath, fileName)
