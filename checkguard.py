#!/usr/bin/env python

import argparse
import crules
import headerfind

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

def printNameIfGuardless(filePath, fileName):
	if not isFileProtectedByGuard(filePath, crules.guardSymbol(fileName)):
		print filePath

def main():
	parser = argparse.ArgumentParser(
		description='Find C or C++ header files with incorrect or missing include guards.')
	parser.add_argument('directory', 
		help='the root directory of the tree to search')
	parser.add_argument('--exclude', 
		help='exclude the given path, allowing for wildcards')
	args = parser.parse_args()
	
	headerfind.applyToHeaders(printNameIfGuardless, args.directory, args.exclude)

if __name__ == '__main__':
	main()
