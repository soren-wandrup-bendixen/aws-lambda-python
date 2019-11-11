# File_name: lambda_function.py
# Purpose: Lambda function to stop all aws services	that cost money	in dev and test
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from CloudWatch event rule	scheduled :	cron( 0	18,19 ? * * * ) 
# Total time to run per execution is 10 minutes. And is set to run twice a day. 

# To be developed
# https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html
# stop_fargate
# Elastic Beanstalk is designed to ensure that all the resources that you need are running, which means that it automatically relaunches any services that you stop. To avoid this, you must terminate your Elastic Beanstalk environment before you terminate resources that Elastic Beanstalk has created
# Services Started in AWS OpsWorks
# If you use the AWS OpsWorks environment to create AWS resources, you must use AWS OpsWorks to terminate those resources or AWS OpsWorks restarts them. For example, if you use AWS OpsWorks to create an Amazon EC2 instance, but then terminate it by using the Amazon EC2 console, the AWS OpsWorks auto healing feature categorizes the instance as failed and restarts it. For more information, see AWS OpsWorks User Guide.
# stop_cloudfront (stop_stack_set_operation)
# stop_alexaforbusiness
# stop_llearning
# make snapshot of elastic search	 before delete
# stop_support root account, report if not free

import datetime
print ('Start time:	' + str(datetime.datetime.now()))

import json
import simple_notification  
import traceback

import get_list_of_possible_resources
import all_region_names
import stop_autoscaling
import stop_elb
import stop_ecs
import stop_eks
import stop_ec2
import stop_nat_gateway
import stop_sagemaker
import stop_robomaker
import stop_rds
import stop_emr
import stop_dax
import stop_kinesis
import stop_kinesisanalytics 
import stop_elasticache
import stop_glue
import stop_elastisearch
import stop_dms
import stop_redshift
import stop_neptune
import stop_batch
import stop_personalize
import stop_shield
import stop_lightsail
import stop_sdb
import stop_dynamodb
import stop_datapipeline
import stop_qldb

def	lambda_handler(event, context):
	RunningInstances =	[]
	instanceList = ''
	try: 
		# only in play when a list of clients is wanted. 
		#get_list_of_possible_resources.fail_with_list('?')
		region_names = all_region_names.get_list('ec2',event['region_set'])
		# region_names = ['us-east-1'] # for simple one region testing; N. Virginia
		# region_names = ['us-west-2'] # for simple one region testing; Oregon
		# region_names = ['eu-north-1'] # for simple one region testing; Stockholm
		# region_names = ['me-south-1'] # for simple one region testing; Bahrain
		# region_names = ['ap-east-1'] # for simple one region testing; Hongkong
		for region_name_ in region_names:
			# RunningInstances.append( str(event['region_set']) + '#' + region_name_ + '#' )
			print (region_name_ + ' time:	' + str(datetime.datetime.now()))
			stop_dynamodb.change_billing_mode('dynamodb', region_name_, RunningInstances)
			stop_datapipeline.inactivate_pipelines('datapipeline', region_name_, RunningInstances)
			stop_qldb.delete_ledgers('qldb', region_name_, RunningInstances)
			stop_autoscaling.suspend_processes('autoscaling', region_name_, RunningInstances)
			stop_batch.disable_job_queues('batch', region_name_, RunningInstances)
			stop_emr.stop_clusters('emr', region_name_, RunningInstances) # Stop EMR before ec2's otherwise the ec2 of emr will be terminated individually
			stop_elb.delete_instances('elb', region_name_,	RunningInstances) # Delete load balancers
			stop_elb.delete_instances('elbv2', region_name_,	RunningInstances) # Delete load balancers
			stop_ecs.stop_instances('ecs', region_name_,	RunningInstances) # Stop: Amazon Elastic Container Service (ECS)
			stop_eks.delete_clusters('eks', region_name_,	RunningInstances) # Stop: Amazon Elastic Container Service for Kubernetes CreateOperation
			stop_ec2.stop_instances('ec2', region_name_,	RunningInstances)
			stop_nat_gateway.delete_ec2_nat_gateways('ec2', region_name_,	RunningInstances) # Stop: Amazon Elastic Compute Cloud NatGateway
			stop_sagemaker.stop_jobs('sagemaker', region_name_, RunningInstances)
			stop_robomaker.stop_jobs('robomaker', region_name_, RunningInstances)
			stop_lightsail.stop_instances('lightsail', region_name_, RunningInstances)
			stop_lightsail.stop_relational_databases('lightsail', region_name_, RunningInstances)
			stop_lightsail.autostart_relational_databases('lightsail', region_name_, RunningInstances)
			stop_rds.stop_instances('rds', region_name_, RunningInstances)
			stop_rds.autostart_instances('rds', region_name_, RunningInstances)
			stop_rds.stop_clusters('rds', region_name_, RunningInstances)
			stop_rds.autostart_clusters('rds', region_name_, RunningInstances)
			stop_rds.stop_clusters('docdb', region_name_, RunningInstances) # stop docdb - same logic as rds cluster
			stop_sdb.delete_domains('sdb', region_name_, RunningInstances) # stops simpleDb (deletes doains) started when performing debug of EMR!
			stop_dax.delete_clusters('dax', region_name_, RunningInstances)
			stop_kinesis.delete_streams('kinesis', region_name_, RunningInstances)	
			stop_kinesisanalytics.stop_applications('kinesisanalytics', region_name_, RunningInstances)	
			stop_elasticache.delete_clusters('elasticache', region_name_,	RunningInstances)
			stop_glue.stop_jobs('glue', region_name_,	RunningInstances)
			stop_elastisearch.delete_domains('es', region_name_,	RunningInstances) # ElasticSearch
			stop_dms.delete_instances('dms', region_name_,	RunningInstances) # Database Migration Service
			# stop_redshift.change_to_smallest('redshift', region_name_,	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
			stop_redshift.delete_clusters('redshift', region_name_,	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
			stop_neptune.delete_clusters('neptune', region_name_,	RunningInstances)	
			stop_neptune.delete_instances('neptune', region_name_, RunningInstances)
			stop_personalize.delete_campaigns('personalize', region_name_, RunningInstances)
		# Global services	
		stop_shield.delete_advanced('shield', RunningInstances) # WAF shield
		if	len(RunningInstances) >	0:
			instanceList = json.dumps(RunningInstances)
			simple_notification.send_info(instanceList)
		statusCode = 200
	except Exception as exception:
		if	len(RunningInstances) >	0:
			instanceList = json.dumps(RunningInstances)
		simple_notification.send_info(instanceList + ' - exception ' + traceback.format_exc() )
		#raise exception 
		statusCode = 404
	print ('End time:	' + str(datetime.datetime.now()))
	return	{
		"statusCode":	statusCode,
		"body": instanceList 
	}


