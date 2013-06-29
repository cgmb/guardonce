#!python

import os
import argparse
import shutil
import filecmp
import difflib
import sys

parser = argparse.ArgumentParser(
	description='Run the given script and check its output matches an expected result set.')
parser.add_argument('script',
	help='the script command')
parser.add_argument('input',
	help='the input directory of the script')
parser.add_argument('expected',
	help='the expected directory tree')
args = parser.parse_args()

# http://youtu.be/k3-zaTr6OUo
output = os.path.join("danger_zone/", args.input)
shutil.rmtree(output, True)
shutil.copytree(args.input, output)

os.system("python " + args.script + " " + output)

dcmp = filecmp.dircmp(output, args.expected)
for f in dcmp.diff_files:
	with open(os.path.join(output, f), 'r') as leftFile:
		with open(os.path.join(args.expected, f), 'r') as rightFile:
			for line in difflib.unified_diff(leftFile.readlines(), rightFile.readlines(), 
											fromfile=leftFile.name, tofile=rightFile.name):
				sys.stdout.write(line)
