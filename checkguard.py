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
	parser.add_argument('files',
		nargs='+',
		help='the file(s) to check; directories require the recursive option')
	parser.add_argument('-r',
		action='store_true',
		dest='recursive',
		help='recursively search directories for headers')
	parser.add_argument('--exclude', 
		help='exclude the given path, allowing for wildcards')
	args = parser.parse_args(arglist)
	
	for fileName in args.files:
		if os.path.isfile(fileName):
			printNameIfGuardless(fileName, os.path.basename(fileName))
		elif os.path.isdir(fileName):
			if args.recursive:
				headerfind.applyToHeaders(printNameIfGuardless, fileName, args.exclude)
			else:
				print >> sys.stderr, ("'" + fileName + "'"
					" is a directory. Search it for headers with -r")

if __name__ == '__main__':
	main(sys.argv[1:])
