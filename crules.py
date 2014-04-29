#!/usr/bin/env python

def guardSymbol(fileName):
	'''The expected include guard symbol for a given file.

	Returns an include guard symbol as a string.
	fileName is the name of the file being guarded,
	and does not include any directory names.
	'''
	return fileName.upper().replace('.', '_')

def isHeaderFile(fileName):
	'''Returns true if the given file is identified as a C/C++ header file.'''
	return fileName.endswith('.h') or fileName.endswith('.hpp')
