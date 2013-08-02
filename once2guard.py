#!/usr/bin/env python

import os
import argparse
from os.path import join
from fnmatch import fnmatch
import crules

parser = argparse.ArgumentParser(
	description='Replace #pragma once with C and C++ include guards.')
parser.add_argument('directory', 
	help='the root directory of the tree to search')
parser.add_argument('--exclude', 
	help='exclude the given path, allowing for wildcards')
args = parser.parse_args()

def findOnce(contents):
	token = '#pragma once'
	index = contents.find(token)
	return index, index + len(token)

def findEndifInsertLocation(contents):
	if contents.endswith('\n\n'):
		return len(contents)-1, True
	else:
		return len(contents), False

def getNewContents(contents, desiredGuard):
	onceStart, onceEnd = findOnce(contents)
	if onceStart < 0:
		return contents
	endifInsert, foundSpot = findEndifInsertLocation(contents)
	return (contents[:onceStart] 
		+ '#ifndef ' + desiredGuard + '\n'
		+ '#define ' + desiredGuard
		+ contents[onceEnd:endifInsert] 
		+ '\n#endif\n')

def findAndReplaceGuard(fileName, desiredGuard):
	if crules.isHeaderFile(fileName):
		with open(fileName, 'r+') as f:
			contents = f.read()
			newContents = getNewContents(contents, desiredGuard)
			if contents != newContents:
				f.truncate(len(newContents))
				f.seek(0)
				f.write(newContents)


for root, dirs, files in os.walk(args.directory):
	for fileName in files:
		filePath = join(root,fileName)
		if args.exclude and fnmatch(filePath, args.exclude):
			continue
		findAndReplaceGuard(filePath, crules.guardSymbol(fileName))
