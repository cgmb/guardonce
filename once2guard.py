#!/usr/bin/env python

import argparse
import headerfind
import crules
import sys
import os

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

def main(arglist=None):
	parser = argparse.ArgumentParser(
		description='Replace #pragma once with C and C++ include guards.')
	headerfind.addArgs(parser)
	args = parser.parse_args(arglist)
	headerfind.processHeaders(args, findAndReplaceGuard)

if __name__ == '__main__':
	main()
