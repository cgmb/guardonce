#!/usr/bin/env python

def guardSymbol(fileName):
	return fileName.upper().replace('.', '_')

def isHeaderFile(fileName):
	return fileName.endswith('.h') or fileName.endswith('.hpp')
