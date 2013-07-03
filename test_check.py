#!python

import os
import shutil
import difflib
import sys
import subprocess

def testCheckGuard(directory, expectedResults):
	inputDir = os.path.join("danger_zone/", directory)
	shutil.rmtree(inputDir, True)
	shutil.copytree(directory, inputDir)

	result = subprocess.check_output(['python', 'check_guard.py', inputDir])

	diffResults = difflib.unified_diff(result, expectedResults)
	foundDifferences = False
	for line in diffResults:
		sys.stdout.write(line)
		foundDifferences = True
	return foundDifferences

testCheckGuard('once_tree','danger_zone/once_tree/thing.h\n')
testCheckGuard('guard_tree','')
