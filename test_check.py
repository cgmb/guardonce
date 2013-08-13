#!/usr/bin/env python

import os
import shutil
import sys
import checkguard
import unittest
from collections import namedtuple
from textwrap import dedent
from StringIO import StringIO

Output = namedtuple('Output', ['stdout', 'stderr'])

def setupDangerZone(inputDir):
	zoneDir = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(zoneDir, True)
	shutil.copytree(inputDir, zoneDir)
	return zoneDir

def runCheckGuardWithArgstring(argstring):
	checkguard.main(argstring.split())
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def runCheckGuard(directory, exclusions=None):
	checkDir = setupDangerZone(directory)

	invokation = ['-r', checkDir]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	checkguard.main(invokation)
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def runCheckGuardOnFile(inputFile):
	dirName, baseName = os.path.split(inputFile)
	checkDir = setupDangerZone(dirName)
	checkFile = os.path.join(checkDir, baseName)

	invokation = [checkFile]
	checkguard.main(invokation)
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

class TestCheckGuard(unittest.TestCase):

	def setUp(self):
		self.saved_out = sys.stdout
		sys.stdout = StringIO()

		self.saved_err = sys.stderr
		sys.stderr = StringIO()

	def tearDown(self):
		sys.stdout = self.saved_out
		sys.stderr = self.saved_err

	def test_standard_guard_file(self):
		self.assertEqual(runCheckGuardOnFile('guard_tree/BasicHeader.h').stdout, dedent(
		'''\
		'''))

	def test_mismatched_guard_file(self):
		self.assertEqual(runCheckGuardOnFile('guard_tree/mismatched_name.h').stdout, dedent(
		'''\
		danger_zone/guard_tree/mismatched_name.h
		'''))

	def test_non_header_file(self):
		self.assertEqual(runCheckGuardOnFile('guard_tree/non_header_file.txt').stdout, dedent(
		'''\
		danger_zone/guard_tree/non_header_file.txt
		'''))

	def test_once_tree(self):
		self.assertEqual(runCheckGuard('once_tree').stdout, dedent(
		'''\
		danger_zone/once_tree/mismatched_name.h
		danger_zone/once_tree/BasicHeader.h
		'''))

	def test_guard_tree(self):
		self.assertEqual(runCheckGuard('guard_tree').stdout, dedent(
		'''\
		danger_zone/guard_tree/mismatched_name.h
		'''))

	def test_exclusion_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/mismatched_name.h').stdout, dedent(
		''))

	def test_exclusion_no_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/some_other_name.h').stdout, dedent(
		'''\
		danger_zone/guard_tree/mismatched_name.h
		'''))

	def test_error_on_passing_file_as_directory(self):
		self.assertEqual(runCheckGuardWithArgstring('-r guard_tree/BasicHeader.h').stderr, 
			"[Errno 20] Not a directory: 'guard_tree/BasicHeader.h'\n")

	def test_error_on_passing_directory_as_file(self):
		self.assertEqual(runCheckGuardWithArgstring('guard_tree').stderr, 
			"[Errno 21] Is a directory: 'guard_tree'\n")

if __name__ == '__main__':
	unittest.main()
