# File_name: lambda_handler.py
# Purpose: Lambda function to stop all aws services	that cost money	in dev and test
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from CloudWatch event rule	scheduled :	cron( 0	18 ? * * * ) 

import botocore
import boto3
 
print("boto3 version:"+boto3.__version__)
print("botocore	version:"+botocore.__version__)
 

import json
import stop_ec2
import stop_sagemaker
import stop_robomaker
import simple_notification

def	suspend_autoscale():
  response = client.suspend_processes(
	  AutoScalingGroupName='string',
	  ScalingProcesses=[
		  'string',
	  ]
  )
  return 
  
  
def	lambda_handler(event, context):

	RunningInstances =	[]
	# "[\"cloudformation\", \"cloudwatch\", \"dynamodb\", \"ec2\",	\"glacier\", \"iam\", \"opsworks\",	\"s3\",	\"sns\", \"sqs\"]"
	#session =	boto3.Session()
	#available_resources =	session.get_available_resources()
	#instanceList = json.dumps(available_resources)
	# stop_autoscale.suspend_autoscale()
	stop_ec2.stop_instances('ec2',	RunningInstances)
	stop_sagemaker.stop_jobs('sagemaker', RunningInstances)
	stop_robomaker.stop_jobs('robomaker',RunningInstances)
	if	len(RunningInstances) >	0:
		instanceList = json.dumps(RunningInstances)
		simple_notification.send_info(instanceList)
	else:
		instanceList = ''

	return	{
		"statusCode":	200,
		"body": instanceList 
	}
