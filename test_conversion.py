#!/usr/bin/env python

import os
import shutil
import filecmp
import difflib
import sys
import guard2once
import once2guard
import unittest

def setupDangerZone(inputDir):
	# http://youtu.be/k3-zaTr6OUo
	output = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(output, True)
	shutil.copytree(inputDir, output)
	return output

def convertedOutputMatchesExpectations(script,inputDir,expectedDir,exclusions=None):
	output = setupDangerZone(inputDir)

	invokation = [output]
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

class TestConversion(unittest.TestCase):

	def test_once2guard(self):
		self.assertTrue(convertedOutputMatchesExpectations(
			once2guard.main, 'once_tree', 'guard_tree'))

	def test_guard2once(self):
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
