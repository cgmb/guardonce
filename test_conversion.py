#!/usr/bin/env python

import os
import shutil
import filecmp
import difflib
import sys
import subprocess

def setupDangerZone(inputDir):
	# http://youtu.be/k3-zaTr6OUo
	output = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(output, True)
	shutil.copytree(inputDir, output)
	return output

def testConversion(script,inputDir,expectedDir,exclusions=None):
	output = setupDangerZone(inputDir)

	invokation = ['python', script, output]
	if exclusions is not None:
		invokation.append('--exclude=' + exclusions)
	subprocess.check_output(invokation)

	dcmp = filecmp.dircmp(output, expectedDir)
	for f in dcmp.diff_files:
		with open(os.path.join(output, f), 'r') as leftFile:
			with open(os.path.join(expectedDir, f), 'r') as rightFile:
				for line in difflib.unified_diff(leftFile.readlines(), rightFile.readlines(), 
												fromfile=leftFile.name, tofile=rightFile.name):
					sys.stdout.write(line)

testConversion('once2guard.py', 'once_tree', 'guard_tree')
testConversion('guard2once.py', 'guard_tree', 'once_tree')
testConversion('once2guard.py', 'exclusion_tree/once', 'exclusion_tree/once_expected', 
	'*/ExcludedHeader.h')
testConversion('guard2once.py', 'exclusion_tree/guard', 'exclusion_tree/guard_expected', 
	'*/ExcludedHeader.h')
