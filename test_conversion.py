#!/usr/bin/env python

import os
import shutil
import filecmp
import difflib
import sys
import guard2once
import once2guard
import unittest
from collections import namedtuple
from StringIO import StringIO

Output = namedtuple('Output', ['stdout', 'stderr'])

def setupDangerZone(inputPath):
	# http://youtu.be/k3-zaTr6OUo
	if os.path.isdir(inputPath):
		output = os.path.join('danger_zone', inputPath)
		shutil.rmtree(output, True)
		shutil.copytree(inputPath, output)
		return output
	return inputPath

def setupFilesInDangerZone(inputPaths):
	outputPaths = []
	for path in inputPaths:
		if os.path.isfile(path):
			dirName, baseName = os.path.split(path)
			checkDir = setupDangerZone(dirName)
			outputPaths.append(os.path.join(checkDir, baseName))
		else:
			raise Exception('Only files supported')
	return outputPaths

def convertedOutputMatchesExpectations(script,inputPath,expectedDir,exclusions=None):
	output = setupDangerZone(inputPath)

	invokation = ['-r', output]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	script.main(invokation)

	dcmp = filecmp.dircmp(output, expectedDir)
	noDifferences = True
	for f in dcmp.diff_files:
		with open(os.path.join(output, f), 'r') as leftFile:
			with open(os.path.join(expectedDir, f), 'r') as rightFile:
				for line in difflib.unified_diff(leftFile.readlines(), rightFile.readlines(), 
												fromfile=leftFile.name, tofile=rightFile.name):
					noDifferences = False
					sys.stdout.write(line)
	return noDifferences

def runScript(script,inputFile,recursive=False):
	dirName, baseName = os.path.split(inputFile)
	checkDir = setupDangerZone(dirName)
	transformFile = os.path.join(checkDir, baseName)

	invokation = [transformFile]
	if recursive:
		invokation.append('-r')
	script.main(invokation)
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def contentsOf(fileName):
	with open(fileName, 'r') as f:
		return f.read()

def runWithArgstring(script,argstring):
	script.main(argstring.split())
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

class TestConversion(unittest.TestCase):

	def setUp(self):
		self.saved_out = sys.stdout
		sys.stdout = StringIO()

		self.saved_err = sys.stderr
		sys.stderr = StringIO()

	def tearDown(self):
		sys.stdout = self.saved_out
		sys.stderr = self.saved_err

	def captured_stdout():
		return sys.stdout.getvalue()

	def captured_stderr():
		return sys.stderr.getvalue()

	def test_once2guard_standard_file(self):
		runScript(once2guard, 'once_tree/BasicHeader.h')
		self.assertMultiLineEqual(
			contentsOf('danger_zone/once_tree/BasicHeader.h'), 
			contentsOf('guard_tree/BasicHeader.h'))

	def test_guard2once_standard_file(self):
		runScript(guard2once, 'guard_tree/BasicHeader.h')
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/BasicHeader.h'), 
			contentsOf('once_tree/BasicHeader.h'))

	def test_once2guard_multi_file(self):
		files = setupFilesInDangerZone(['once_tree/mismatched_name.h', 'once_tree/BasicHeader.h'])
		runWithArgstring(once2guard, ' '.join(files))
		self.assertMultiLineEqual(
			contentsOf('danger_zone/once_tree/BasicHeader.h'), 
			contentsOf('guard_tree/BasicHeader.h'))
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/mismatched_name.h'), 
			contentsOf('guard_tree/mismatched_name.h'))

	def test_guard2once_multi_file(self):
		files = setupFilesInDangerZone(['guard_tree/mismatched_name.h', 'guard_tree/BasicHeader.h'])
		runWithArgstring(guard2once, ' '.join(files))
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/BasicHeader.h'), 
			contentsOf('once_tree/BasicHeader.h'))
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/mismatched_name.h'), 
			contentsOf('once_tree/mismatched_name.h'))

	def test_once2guard_directory_as_file(self):
		self.assertEqual(runScript(once2guard, 'once_tree').stderr,
			"'once_tree' is a directory. Search it for headers with -r\n")

	def test_once2guard_standard_file_recursive(self):
		runScript(once2guard, 'once_tree/BasicHeader.h', recursive=True)
		self.assertMultiLineEqual(
			contentsOf('danger_zone/once_tree/BasicHeader.h'), 
			contentsOf('guard_tree/BasicHeader.h'))

	def test_guard2once_directory_as_file(self):
		self.assertEqual(runWithArgstring(guard2once, 'guard_tree').stderr,
			"'guard_tree' is a directory. Search it for headers with -r\n")

	def test_guard2once_standard_file_recursive(self):
		runScript(guard2once, 'guard_tree/BasicHeader.h', recursive=True)
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/BasicHeader.h'), 
			contentsOf('once_tree/BasicHeader.h'))

	def test_guard2once_no_newline_at_eof(self):
		runScript(guard2once, 'irreversable_tree/no_newline_at_eof/BasicHeader.h')
		self.assertMultiLineEqual(
			contentsOf('danger_zone/irreversable_tree/no_newline_at_eof/BasicHeader.h'), 
			contentsOf('once_tree/BasicHeader.h'))

	def test_guard2once_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once, 'guard_tree', 'once_tree'))

	def test_once2guard_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			once2guard, 'once_tree', 'guard_tree'))

	def test_guard2once_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once, 'guard_tree', 'once_tree'))

	def test_once2guard_excludes(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			once2guard, 'exclusion_tree/once', 'exclusion_tree/once_expected', 
			'*/ExcludedHeader.h'))

	def test_guard2once_excludes(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once, 'exclusion_tree/guard', 'exclusion_tree/guard_expected', 
			'*/ExcludedHeader.h'))

if __name__ == '__main__':
	unittest.main()
