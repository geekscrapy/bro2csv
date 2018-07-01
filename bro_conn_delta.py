#!/usr/python

import os
import csv
import pprint
import argparse
import numpy as np
import statistics as stats
import io
from prettytable import PrettyTable as pt

parser = argparse.ArgumentParser(description='Get the delta between two')
parser.add_argument('--csv', action='store_true', required=False, help='Output as CSV')
parser.add_argument('--proto', action='store_true', required=False, default=None, help='Baseline on protocol as well as src and dest hosts')
parser.add_argument('--port', action='store_true', required=False, default=None, help='Baseline on port as well as src and dest hosts')
parser.add_argument('--service', action='store_true', required=False, default=None, help='Baseline on service as well as src and dest hosts')
parser.add_argument('-i', '--input', dest='input', required=True, metavar='./bro_logs/conn.log.csv', type=str, help='Specific bro log path - Works best with conn.log. Must be .log')
args = parser.parse_args()


deltas = {} # { (src, dst, *, *): { 'prev': int, 'delta': [1, 3], 'increment': [0, 12] } }
start = None

with open(args.input, 'r') as f:

	csv_read = csv.DictReader(f)

	for row in csv_read:

		start = float(row['ts']) if not start else start

		proto = row['proto'] if args.proto else None
		port = row['id_resp_p'] if args.port else None
		service = row['service'] if args.service else None

		comm_tuple = ( row['id_orig_h'].strip(), row['id_resp_h'].strip(), proto, port, service )

		if not comm_tuple in deltas:
			deltas[comm_tuple] = { 'prev': float(row['ts']), 'delta': [], 'interval': []}
		else:
			prev = deltas[comm_tuple]['prev']
			deltas[comm_tuple]['delta'].append( float(row['ts']) - prev )
			deltas[comm_tuple]['prev'] = float(row['ts'])
			deltas[comm_tuple]['interval'].append( float(row['ts']) - start )


if args.csv:
	headers = ['connection_tuple', 'interval']

	csv_out = io.BytesIO()
	csv_w = csv.DictWriter(csv_out, headers, dialect='excel', quoting=csv.QUOTE_ALL)
	csv_w.writeheader()

else:
	headers = ['Connection_tuple', 'Occurance', 'Min_delta', 'Max_delta', 'Overall_duration', 'Standard_dev', 'Variance']

	t = pt(headers)
	t.align['Connection_tuple'] = 'l'
	t.align['Min_delta'] = 'l'
	t.align['Max_delta'] = 'l'
	t.align['Overall_duration'] = 'l'
	t.align['Standard_dev'] = 'l'
	t.align['Variance'] = 'l'



for comm_tuple, delta_v in deltas.items():

	delta_list = delta_v['delta']
	occurance = len(delta_list)+1

	# If there is only one comm, this is useless, also disgard
	# comms with only 2 points as this would be classified as beaconing!
	if len(delta_list) < 3:
		continue

	src, dst, proto, port, service = comm_tuple

	if args.csv:

		line = '{0}>{1}'.format(src, dst)
		line += ':{}'.format(port) if port else '' 
		line += '/{}'.format(proto) if proto else '' 
		line += '-{}'.format(service) if service else '' 


		for beacon in delta_v['interval']:

			csv_w.writerow({
				'connection_tuple': line,
				'interval': beacon,
				})
			rows = csv_out.getvalue()[:-1]

	else:

		round_list = [ round(x, 3) for x in delta_list ]
		stdev = stats.stdev(round_list)
		var = stats.variance(round_list)
		min_d = min(round_list)
		max_d = max(round_list)
		o_durr = max(delta_v['interval']) - min(delta_v['interval'])

		line = '{0:<15} > {1:<15}'.format(src, dst)
		line += ' :{:<5}'.format(port) if port else '' 
		line += ' /{:>4}'.format(proto) if proto else '' 
		line += ' ({})'.format(service) if service else '' 

		t.add_row([line, str(occurance),str(min_d), str(max_d), str(stdev), str(o_durr), str(var) ])

if args.csv:
	print(rows)
else:
	print(t)
