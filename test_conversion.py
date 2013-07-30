#!/usr/bin/env python

import os
import shutil
import filecmp
import difflib
import sys


def testConversion(script,inputDir,expectedDir):
	# http://youtu.be/k3-zaTr6OUo
	output = os.path.join("danger_zone/", inputDir)
	shutil.rmtree(output, True)
	shutil.copytree(inputDir, output)

	os.system("python " + script + " " + output)

	dcmp = filecmp.dircmp(output, expectedDir)
	for f in dcmp.diff_files:
		with open(os.path.join(output, f), 'r') as leftFile:
			with open(os.path.join(expectedDir, f), 'r') as rightFile:
				for line in difflib.unified_diff(leftFile.readlines(), rightFile.readlines(), 
												fromfile=leftFile.name, tofile=rightFile.name):
					sys.stdout.write(line)

testConversion('once2guard.py', 'once_tree', 'guard_tree')
testConversion('guard2once.py', 'guard_tree', 'once_tree')
