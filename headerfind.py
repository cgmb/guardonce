#!/usr/bin/env python

import sys
import os
from os.path import join
from fnmatch import fnmatch
from functools import partial
import crules

def printError(error):
	print >> sys.stderr, error

def shouldBeExcluded(filePath, exclusions):
	return any(map(partial(fnmatch, filePath), exclusions))

def applyToHeaders(func,directory,exclusions):
	for root, dirs, files in os.walk(directory, onerror=printError):
		for fileName in files:
			filePath = join(root,fileName)
			if shouldBeExcluded(filePath, exclusions):
				continue
			if crules.isHeaderFile(fileName):
				func(filePath, fileName)

def addArgs(parser):
	parser.add_argument('files',
		nargs='+',
		help='the file(s) to check; directories require the recursive option')
	parser.add_argument('-r','--recursive',
		action='store_true',
		dest='recursive',
		help='recursively search directories for headers')
	parser.add_argument('-e','--exclude', 
		action='append',
		dest='exclusions',
		metavar='exclude',
		default=[],
		help='exclude the given path, allowing for wildcards')

def processHeaders(args, func):
	for fileName in args.files:
		if os.path.isfile(fileName):
			func(fileName, os.path.basename(fileName))
		elif os.path.isdir(fileName):
			if args.recursive:
				applyToHeaders(func, fileName, args.exclusions)
			else:
				print >> sys.stderr, ("'" + fileName + "'"
					" is a directory. Search it for headers with -r")
