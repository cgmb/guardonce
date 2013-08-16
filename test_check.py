#!/usr/bin/env python

import os
import shutil
import sys
import checkguard
import unittest
from collections import namedtuple
from StringIO import StringIO

Output = namedtuple('Output', ['stdout', 'stderr'])

def setupFileInDangerZone(fileName, permissions):
	output = os.path.join('danger_zone/default/')
	shutil.rmtree(output, True)
	os.makedirs(output)
	outputFileName = os.path.join(output, os.path.basename(fileName))
	shutil.copy(fileName, output)
	os.chmod(outputFileName, permissions)
	return outputFileName

def runCheckGuardWithArgstring(argstring):
	checkguard.main(argstring.split())
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def runCheckGuard(directory, exclusions=None):
	invokation = ['-r', directory]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	checkguard.main(invokation)
	return Output(sys.stdout.getvalue(), sys.stderr.getvalue())

def runCheckGuardOnFile(inputFile):
	dirName, baseName = os.path.split(inputFile)
	checkFile = os.path.join(dirName, baseName)

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
		self.assertEqual(runCheckGuardOnFile('guard_tree/BasicHeader.h').stdout,
		'')

	def test_mismatched_guard_file(self):
		self.assertEqual(runCheckGuardOnFile('guard_tree/mismatched_name.h').stdout,
		'guard_tree/mismatched_name.h\n')

	def test_non_header_file(self):
		self.assertEqual(runCheckGuardOnFile('guard_tree/non_header_file.txt').stdout,
		'guard_tree/non_header_file.txt\n')

	def test_multiple_header_files(self):
		self.assertEqual(runCheckGuardWithArgstring('guard_tree/BasicHeader.h '
			'guard_tree/non_header_file.txt guard_tree/mismatched_name.h').stdout,
		'guard_tree/non_header_file.txt\n'
		'guard_tree/mismatched_name.h\n')

	def test_once_tree(self):
		self.assertEqual(runCheckGuard('once_tree').stdout,
		'once_tree/mismatched_name.h\n'
		'once_tree/BasicHeader.h\n')

	def test_guard_tree(self):
		self.assertEqual(runCheckGuard('guard_tree').stdout,
		'guard_tree/mismatched_name.h\n')

	def test_exclusion_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/mismatched_name.h').stdout,
		'')

	def test_exclusion_no_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/some_other_name.h').stdout,
		'guard_tree/mismatched_name.h\n')

	def test_standard_guard_file_with_recursive_search(self):
		self.assertEqual(runCheckGuardWithArgstring('-r guard_tree/BasicHeader.h').stdout,
		'')
		
	def test_mismatched_guard_file_with_recursive_search(self):
		self.assertEqual(runCheckGuardWithArgstring('-r guard_tree/mismatched_name.h').stdout,
		'guard_tree/mismatched_name.h\n')

	def test_error_on_passing_directory_as_file(self):
		self.assertEqual(runCheckGuardWithArgstring('guard_tree').stderr,
		"'guard_tree' is a directory. Search it for headers with -r\n")

	def test_read_only_mismatched_guard_file(self):
		fileName = setupFileInDangerZone('guard_tree/mismatched_name.h', 0444)
		self.assertEqual(runCheckGuardOnFile(fileName).stdout,
			fileName + '\n')

if __name__ == '__main__':
	unittest.main()
