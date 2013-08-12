#!/usr/bin/env python

import argparse
import headerfind
import crules
import sys

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
	with open(filePath, 'r+') as f:
		contents = f.read()
		newContents = getNewContents(contents, crules.guardSymbol(fileName))
		if contents != newContents:
			f.truncate(len(newContents))
			f.seek(0)
			f.write(newContents)

def main(arglist):
	parser = argparse.ArgumentParser(
		description='Replace #pragma once with C and C++ include guards.')
	parser.add_argument('directory', 
		help='the root directory of the tree to search')
	parser.add_argument('--exclude', 
		help='exclude the given path, allowing for wildcards')
	args = parser.parse_args(arglist)

	headerfind.applyToHeaders(findAndReplaceGuard, args.directory, args.exclude)

if __name__ == '__main__':
	main(sys.argv[1:])
