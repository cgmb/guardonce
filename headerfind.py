#!/usr/bin/env python

import os
from os.path import join
from fnmatch import fnmatch
import crules

def applyToHeaders(func,directory,exclude):
	for root, dirs, files in os.walk(directory):
		for fileName in files:
			filePath = join(root,fileName)
			if exclude and fnmatch(filePath, exclude):
				continue
			if crules.isHeaderFile(fileName):
				func(filePath, fileName)
