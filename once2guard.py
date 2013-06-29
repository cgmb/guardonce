#!python

import os
import argparse
from os.path import join

parser = argparse.ArgumentParser(
	description='Replace #pragma once with C and C++ include guards.')
parser.add_argument('directory', 
	help='the root directory of the tree to search')
args = parser.parse_args()

def defineSymbol(fileName):
	return fileName.upper().replace('.', '_')

def isHeaderFile(fileName):
	return fileName.endswith('.h')

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
		+ '#endif\n\n')

def findAndReplaceGuard(fileName, desiredGuard):
	if isHeaderFile(fileName):
		with open(fileName, 'r+') as f:
			contents = f.read()
			newContents = getNewContents(contents, desiredGuard)
			if contents != newContents:
				f.truncate(len(newContents))
				f.seek(0)
				f.write(newContents)


for root, dirs, files in os.walk(args.directory):
	for fileName in files:
		findAndReplaceGuard(join(root,fileName), defineSymbol(fileName))
