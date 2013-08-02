#!/usr/bin/env python

import os
import argparse
from os.path import join
from fnmatch import fnmatch
import crules

parser = argparse.ArgumentParser(
	description='Replace C and C++ include guards with #pragma once.')
parser.add_argument('directory', 
	help='the root directory of the tree to search')
parser.add_argument('--exclude', 
	help='exclude the given path, allowing for wildcards')
args = parser.parse_args()

def findGuard(contents, expectedGuard):
	index = contents.find(expectedGuard)
	if index < 0:
		return -1, -1
	index = contents.rfind('#ifndef', 0, index)
	endIndex = contents.find('#define', index)
	endIndex = contents.find('\n', endIndex)
	return index, endIndex

def findFinalEndif(contents):
	index = contents.rfind('#endif')
	endIndex = contents.find('\n', index) + 1
	return index, endIndex

def getNewContents(contents, expectedGuard):
	defStart, defEnd = findGuard(contents,expectedGuard)
	endifStart, endifEnd = findFinalEndif(contents)
	if defStart < 0 or endifStart < 0:
		return contents
	return (contents[:defStart] 
		+ "#pragma once" 
		+ contents[defEnd:endifStart] 
		+ contents[endifEnd:])

def findAndReplaceGuard(fileName, expectedGuard):
	if crules.isHeaderFile(fileName):
		with open(fileName, 'r+') as f:
			contents = f.read()
			newContents = getNewContents(contents, expectedGuard)
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
