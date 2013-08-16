#!/usr/bin/env python

import argparse
import crules
import headerfind
import sys
import os

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
	with open(fileName, 'r') as f:
		contents = f.read()
		return isContentProtectedByGuard(contents, expectedGuard)

def printNameIfGuardless(filePath, fileName):
	try:
		if not isFileProtectedByGuard(filePath, crules.guardSymbol(fileName)):
			print filePath
	except Exception as e:
		print >> sys.stderr, e

def main(arglist):
	parser = argparse.ArgumentParser(
		description='Find C or C++ header files with incorrect or missing include guards.')
	parser.add_argument('file',
		nargs='?',
		help='the file to check')
	parser.add_argument('-r',
		dest='directory',
		help='the root directory of the tree to search')
	parser.add_argument('--exclude', 
		help='exclude the given path, allowing for wildcards')
	args = parser.parse_args(arglist)
	
	if args.directory is not None:
		headerfind.applyToHeaders(printNameIfGuardless, args.directory, args.exclude)
	
	if args.file is not None:
		printNameIfGuardless(args.file, os.path.basename(args.file))

if __name__ == '__main__':
	main(sys.argv[1:])
