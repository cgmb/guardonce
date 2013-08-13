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

def setupDangerZone(inputDir):
	# http://youtu.be/k3-zaTr6OUo
	output = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(output, True)
	shutil.copytree(inputDir, output)
	return output

def convertedOutputMatchesExpectations(script,inputDir,expectedDir,exclusions=None):
	output = setupDangerZone(inputDir)

	invokation = ['-r', output]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	script(invokation)

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

def runOnFile(script,inputFile):
	dirName, baseName = os.path.split(inputFile)
	checkDir = setupDangerZone(dirName)
	transformFile = os.path.join(checkDir, baseName)

	invokation = [transformFile]
	script(invokation)
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def contentsOf(fileName):
	with open(fileName, 'r') as f:
		return f.read()

def runWithArgstring(script,argstring):
	script(argstring.split())
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

	def test_once2guard_standard_file(self):
		runOnFile(once2guard.main, 'once_tree/BasicHeader.h')
		self.assertMultiLineEqual(
			contentsOf('danger_zone/once_tree/BasicHeader.h'), 
			contentsOf('guard_tree/BasicHeader.h'))

	def test_guard2once_standard_file(self):
		runOnFile(guard2once.main, 'guard_tree/BasicHeader.h')
		self.assertMultiLineEqual(
			contentsOf('danger_zone/guard_tree/BasicHeader.h'), 
			contentsOf('once_tree/BasicHeader.h'))

	def test_once2guard_directory_as_file(self):
		self.assertEqual(runWithArgstring(once2guard.main, 'once_tree').stderr,
			"[Errno 21] Is a directory: 'once_tree'\n")

	def test_once2guard_file_as_directory(self):
		self.assertEqual(runWithArgstring(once2guard.main, '-r once_tree/BasicHeader.h').stderr,
			"[Errno 20] Not a directory: 'once_tree/BasicHeader.h'\n")

	def test_guard2once_directory_as_file(self):
		self.assertEqual(runWithArgstring(guard2once.main, 'guard_tree').stderr,
			"[Errno 21] Is a directory: 'guard_tree'\n")

	def test_guard2once_file_as_directory(self):
		self.assertEqual(runWithArgstring(guard2once.main, '-r guard_tree/BasicHeader.h').stderr,
			"[Errno 20] Not a directory: 'guard_tree/BasicHeader.h'\n")

	def test_guard2once_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once.main, 'guard_tree', 'once_tree'))

	def test_once2guard_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			once2guard.main, 'once_tree', 'guard_tree'))

	def test_guard2once_tree(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once.main, 'guard_tree', 'once_tree'))

	def test_once2guard_excludes(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			once2guard.main, 'exclusion_tree/once', 'exclusion_tree/once_expected', 
			'*/ExcludedHeader.h'))

	def test_guard2once_excludes(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			guard2once.main, 'exclusion_tree/guard', 'exclusion_tree/guard_expected', 
			'*/ExcludedHeader.h'))

if __name__ == '__main__':
	unittest.main()
