# File_name: lambda_handler.py
# Purpose: Lambda function to stop all aws services	that cost money	in dev and test
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from CloudWatch event rule	scheduled :	cron( 0	18 ? * * * ) 
# Currently not stopping 
# 1. dynamodb (no support for stop). What does a dynomodb cost if its not getting used? 
# 2. vpc (no cost)
# 3. Can not stop s3. Have to drop s3 to do that and that is not wanted.


# To be developed
# stop_batch
# stop_cloudfront stop_stack_set_operation
# stop_docdb
# stop_elasticache
# stop_elastisearch
# stop_firehose
# stop_glue
# stop_iot
# stop_kinesis
# stop_machinelearning
# stop_redshift
# stop_simpledb
# change_waf change to free edition

import botocore
import boto3
 
print("boto3 version:"+boto3.__version__)
print("botocore	version:"+botocore.__version__)
 

import json
import stop_autoscaling
import stop_ecs
import delete_eks
import stop_ec2
import delete_nat_gateway
import stop_sagemaker
import stop_robomaker
import stop_rds
import simple_notification  
  
def	lambda_handler(event, context):

	RunningInstances =	[]
	# "[\"cloudformation\", \"cloudwatch\", \"dynamodb\", \"ec2\",	\"glacier\", \"iam\", \"opsworks\",	\"s3\",	\"sns\", \"sqs\"]"
	#session =	boto3.Session()
	#available_resources =	session.get_available_resources()
	#instanceList = json.dumps(available_resources)
	stop_autoscaling.suspend_processes('autoscaling',	RunningInstances)
	# Stop: load balancers
	stop_ecs.stop_instances('ecs',	RunningInstances)
	# Stop: Amazon Elastic Container Service for Kubernetes CreateOperation
	delete_eks.stop_instances('eks',	RunningInstances)
	stop_ec2.stop_instances('ec2',	RunningInstances)
	# Stop: Amazon Elastic Compute Cloud NatGateway
	delete_nat_gateway.delete_ec2_nat_gateways('ec2',	RunningInstances)
	stop_sagemaker.stop_jobs('sagemaker', RunningInstances)
	stop_robomaker.stop_jobs('robomaker',RunningInstances)
	
	stop_rds.stop_instances('rds',RunningInstances)
	stop_rds.autostart_instances('rds',RunningInstances)
	stop_rds.stop_clusters('rds',RunningInstances)
	stop_rds.autostart_clusters('rds',RunningInstances)
	
	if	len(RunningInstances) >	0:
		instanceList = json.dumps(RunningInstances)
		simple_notification.send_info(instanceList)
	else:
		instanceList = ''

	return	{
		"statusCode":	200,
		"body": instanceList 
	}


