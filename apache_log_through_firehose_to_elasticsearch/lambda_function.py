# File_name: lambda_function.py
# Purpose: Lambda function to transform apache log to elasticsearch format. 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from Kinesis firehose 


import base64
import json
import re

import os
import logging

import datetime
print ('Start time:	' + str(datetime.datetime.now()))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#convert string to hex
toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])


def safe_cast(val, to_type, default=None):
	try:
		return to_type(val)
	except (ValueError, TypeError):
		logger.info(str(val) + ' error ' + str(to_type))
		return default

def	lambda_handler(event, context):
#	logger.info('## ENVIRONMENT VARIABLES')
#	logger.info(os.environ)
#	logger.info('## EVENT')
#	logger.info(event)

	output	= []
	succeeded_record_count	= 0
	failed_record_count = 0

	for record	in event['records']:
		log_line = base64.b64decode(record['data']).decode('utf-8') 
#		logger.info(log_line)
#		logger.info(toHex(log_line))
		# regular_expression = re.compile(r"^\[(\w+)\]\s(\S+)\s(\S+)\s(\S+) - - \[(\S+) (\S+)\] \"(\S+) (\S+) (\S+)\" (\d+) (\d+) *")
		regular_expression = re.compile(r"^(\S+) - - \[(\S+) (\S+)\] \"(\S+) (\S+) (\S+)\" (\d+) (\S+) *")
		match	= regular_expression.match(log_line)
		if match:
#			for	i in range(1,8) :
#				logger.info(str(i) + '#' + match.group(i))
			succeeded_record_count += 1
			test_date = ( datetime.datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S')).isoformat()
			# 27/Jan/2020:15:08:29
			data_field =	{
				'host':	match.group(1),
				'timestamp': ( datetime.datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S')).isoformat(),
				'timestamp_utc': ( datetime.datetime.strptime(match.group(2) + ' ' + match.group(3), '%d/%b/%Y:%H:%M:%S %z')).isoformat(),
				'request': match.group(4) + ' ' + match.group(5) + ' ' + match.group(6),
				'response': safe_cast(match.group(7),int,0),
				'bytes': safe_cast(match.group(8),int,0)
			}
			log_line_json_encoded = base64.b64encode(json.dumps(data_field).encode('utf-8'))
			output_record = {
				'recordId':	record['recordId'],
				'result': 'Ok',
				'data':	log_line_json_encoded.decode('utf-8')
			}
		else:
			logger.info('Parsing failed')
			logger.info(log_line)
			logger.info(toHex(log_line))
			failed_record_count +=1
			output_record = {
				'recordId':	record['recordId'],
				'result': 'ProcessingFailed',
				'data':	record['data']
			}
			
		output.append(output_record)
#		if succeeded_record_count > 3:
#			break
	logger.info('Processing completed.	 Successful	records	{},	Failed records {}.'.format(succeeded_record_count, failed_record_count))
	logger.info(output)
	return	{'records':	output}


 


