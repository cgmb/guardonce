#!/usr/bin/env python

import os
import shutil
import sys
import checkguard
import unittest
from textwrap import dedent
from StringIO import StringIO

def setupDangerZone(inputDir):
	zoneDir = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(zoneDir, True)
	shutil.copytree(inputDir, zoneDir)
	return zoneDir

def runCheckGuard(directory, exclusions=None):
	checkDir = setupDangerZone(directory)

	invokation = [checkDir]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	checkguard.main(invokation)
	return sys.stdout.getvalue()

class TestCheckGuard(unittest.TestCase):

	def setUp(self):
		self.saved_out = sys.stdout
		sys.stdout = StringIO()

	def tearDown(self):
		sys.stdout = self.saved_out

	def test_once_tree(self):
		self.assertEqual(runCheckGuard('once_tree'), dedent(
		'''\
		danger_zone/once_tree/mismatched_name.h
		danger_zone/once_tree/BasicHeader.h
		'''))

	def test_guard_tree(self):
		self.assertEqual(runCheckGuard('guard_tree'), dedent(
		'''\
		danger_zone/guard_tree/mismatched_name.h
		'''))

	def test_exclusion_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/mismatched_name.h'), dedent(
		''))

	def test_exclusion_no_match(self):
		self.assertEqual(runCheckGuard('guard_tree', '*/some_other_name.h'), dedent(
		'''\
		danger_zone/guard_tree/mismatched_name.h
		'''))

if __name__ == '__main__':
	unittest.main()
