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
	if endIndex == 0:
		endIndex = len(contents)
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

def findAndReplaceGuard(filePath, fileName):
	try:
		with open(filePath, 'r+') as f:
			contents = f.read()
			newContents = getNewContents(contents, crules.guardSymbol(fileName))
			if contents != newContents:
				f.truncate(len(newContents))
				f.seek(0)
				f.write(newContents)
	except Exception as e:
		print >> sys.stderr, e

def main(arglist):
	parser = argparse.ArgumentParser(
		description='Replace C and C++ include guards with #pragma once.')
	headerfind.addArgs(parser)
	args = parser.parse_args(arglist)
	headerfind.processHeaders(args, findAndReplaceGuard)

if __name__ == '__main__':
	main(sys.argv[1:])
