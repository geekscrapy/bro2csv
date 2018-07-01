#!/usr/bin/python

import os
import glob
import ntpath
import argparse
from parsebrologs import ParseBroLogs

parser = argparse.ArgumentParser(description='Translate bro logs (TSV) to CSV')
parser.add_argument('-i', '--input', dest='input', nargs = '+', required=True, metavar='./bro_logs/http.log', type=str, help='Specific bro log path - individual file or directory. Must be .log')
parser.add_argument('-f', '--fields', type=str, nargs = '+', metavar='host', default=[], required=False, help='Bro output fields')
parser.add_argument('--overwrite', action='store_true', required=False, help='Overwrite any existing files')
parser.add_argument('--stdo', action='store_true', required=False, help='Print to standard out (as csv)')
parser.add_argument('--cwd', action='store_true', required=False, help='Save files to the current working directory instead of beside original files.')
parser.add_argument('--glob', type=str, default='*.log', metavar='"*.log"', required=False, help='Glob for bro logs. Must be quoted, e.g. "*.log" - can\'t be used when the input is a file (obviously...)')
args = parser.parse_args()


files = []

for i in args.input:

  if os.path.isdir(i):
    files += glob.glob('{}{}'.format(i, args.glob))
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

    # print(dir(log_data))
    # exit()

  except Exception as e:
    print('Error ({}): {}'.format(e,f))
    continue

  if args.stdo:
    print(log_data.to_escaped_csv(safe_headers=True))

  else:

    if (os.path.isfile(new_file) and args.overwrite) or (not os.path.isfile(new_file)):

      print('Parsing: {}'.format(f))

      with open(new_file, 'w') as outfile:
        outfile.write(log_data.to_escaped_csv(safe_headers=True))

      print('Written: {}.csv'.format(f))

    else:
      print('Not overwriting: {}'.format(new_file))
