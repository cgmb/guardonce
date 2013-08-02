#!/usr/bin/env python

import os
import shutil
import difflib
import sys
import subprocess

def testCheckGuard(directory, expectedResults, exclusions=None):
	inputDir = os.path.join("danger_zone/", directory)
	shutil.rmtree(inputDir, True)
	shutil.copytree(directory, inputDir)

	invokation = ['python', 'checkguard.py', inputDir]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	result = subprocess.check_output(invokation)

	diffResults = difflib.unified_diff(result, expectedResults)
	for line in diffResults:
		sys.stdout.write(line)

testCheckGuard('once_tree',
'''\
danger_zone/once_tree/mismatched_name.h
danger_zone/once_tree/BasicHeader.h
''')

testCheckGuard('guard_tree',
'''\
danger_zone/guard_tree/mismatched_name.h
''')

testCheckGuard('guard_tree',
'''''', 
'*/mismatched_name.h')

testCheckGuard('guard_tree',
'''\
danger_zone/guard_tree/mismatched_name.h
''', 
'*/some_other_name.h')
