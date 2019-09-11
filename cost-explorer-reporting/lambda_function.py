# File_name: lambda_function.py
# Purpose: Lambda function to generate cost and usage report adhoc from lambda test or scheduled from CloudWatch
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-11-09
# Called from CloudWatch event rule	scheduled :	cron( 0	8 ? * * 1 ) # run every monday at 0800
# Total time to run per execution is 5 seconds.  


import datetime
print ('Start time:	' + str(datetime.datetime.now()))

import os
import json
import boto3
import datetime
from datetime import timedelta

import cost_explorer
import make_excel
import simple_notification


def lambda_handler(event, context):
# Can not use HOURLY, because its not supported publically yet!
#		  datetime.datetime.now()-timedelta(days=100) # start_date_
#		, datetime.datetime.now()-timedelta(days=1) # end_date_
#		, 'HOURLY' # granaluarity_

	client = boto3.client('ce')
	# Get the cost from Cost explorer
	cost_usage_response = cost_explorer.extraxt_full ( 
		  datetime.date.today()-timedelta(days=100) # start_date_
		, datetime.date.today()-timedelta(days=1) # end_date_
		, 'DAILY' # granaluarity_
		, {"Not": {"Dimensions": {"Key": "RECORD_TYPE","Values": ["Credit", "Refund", "Upfront", "Support"]}}} # filter_
	)
	# Create a Pandas dataframe from cost_usage_response.
	dataFrame = make_excel.make_detail_dataframe ( cost_usage_response )
	# Create a Pandas Excel writer using XlsxWriter as the engine.
	output = make_excel.create_excel_file_in_memory ( dataFrame ) 

	# store sheet on s3
	s3 = boto3.resource('s3')
	s3_file_name = 'cost_usage_' + (datetime.datetime.now()).isoformat('_') + '.xlsx'
	data = output.getvalue()
	s3.Bucket(os.environ.get('S3_BUCKET')).put_object(Key=s3_file_name, Body=data)

	# send link to excel sheetsaved on s3 	
	# simple_notification.send_info( 'https://' + os.environ.get('S3_BUCKET') + '.s3.amazonaws.com/' + s3_file_name )

	print ('End time:	' + str(datetime.datetime.now()))

	return	{
		"statusCode":	200,
		"body": "What ever" 
	}

