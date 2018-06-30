#!/usr/bin/python

from parsebrologs import ParseBroLogs
import argparse
import os, glob, ntpath, io, csv, json

parser = argparse.ArgumentParser(description='Translate bro logs (TSV) to CSV')

parser.add_argument('-i', '--input', dest='input', nargs = '+', required=True, metavar='./bro_logs/http.log', type=str, help='Specific bro log path - individual file or directory. Must be .log')
parser.add_argument('-f', '--fields', type=str, nargs = '+', default=[], required=False, help='Fields to output')
parser.add_argument('--overwrite', action='store_true', required=False, help='Overwrite existing files')
parser.add_argument('--stdo', action='store_true', required=False, help='Print to standard out (as csv)')
parser.add_argument('--cwd', action='store_true', required=False, help='Save files to the current working directory instead of beside original files.')

args = parser.parse_args()


files = []

for i in args.input:

	if os.path.isdir(i):
		files += glob.glob('{}*.log'.format(i))
	else:
		files.append(i)


for f in files:

	if args.cwd:
		new_file = ntpath.basename(f)
	else:
		new_file = '{}.csv'.format(str(f))

	try:
		if len(args.fields) == 0:
			log_data = ParseBroLogs(f)
		else:
			log_data = ParseBroLogs(f, fields=args.fields)

	except Exception as e:
		print('Error ({}): {}'.format(e,f))
		continue

	if args.stdo:
		print(log_data.to_csv())

	else:

		if (os.path.isfile(new_file) and args.overwrite) or (not os.path.isfile(new_file)):

			print('Parsing: {}'.format(f))

			with open(new_file, 'w') as outfile:
				outfile.write(log_data.to_escaped_csv())

			print('Written: {}.csv'.format(f))

		else:
			print('Not overwriting: {}'.format(new_file))
