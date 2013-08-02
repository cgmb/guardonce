#!/usr/bin/env python

import os
import argparse
from os.path import join
from fnmatch import fnmatch
import crules

parser = argparse.ArgumentParser(
	description='Find C or C++ header files with incorrect or missing include guards.')
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

def isContentProtectedByGuard(contents, expectedGuard):
	defStart, defEnd = findGuard(contents,expectedGuard)
	endifStart, endifEnd = findFinalEndif(contents)
	return not (defStart < 0 or endifStart < 0)

def isFileProtectedByGuard(fileName, expectedGuard):
	with open(fileName, 'r+') as f:
		contents = f.read()
		return isContentProtectedByGuard(contents, expectedGuard)

def isProblemFile(filePath, fileName):
	return (crules.isHeaderFile(fileName) and 
		not isFileProtectedByGuard(filePath, crules.guardSymbol(fileName)))

for root, dirs, files in os.walk(args.directory):
	for fileName in files:
		filePath = join(root,fileName)
		if args.exclude and fnmatch(filePath, args.exclude):
				continue
		if isProblemFile(filePath, fileName):
			print filePath
