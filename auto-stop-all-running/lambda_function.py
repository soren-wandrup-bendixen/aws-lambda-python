# File_name: lambda_handler.py
# Purpose: Lambda function to stop all aws services	that cost money	in dev and test
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from CloudWatch event rule	scheduled :	cron( 0	18,19 ? * * * ) 
# Total time to run per execution is 10.4 seconds. And is set to run twice a day. 
# Currently not stopping 
# 1. not stopping dynamodb (no support for stop). You only pay for using it when you access it. But have to delete dax on it! 
# 2. Not stopping lambda, cloudwatch - would kill my self
# 3. Not stopping firehose (kinesis). Only cost meney when data is ingested. So stop that.

# To be developed
# stop_batch - 
# stop_simpledb - will delete the domain calling delete_domain
# stop_cloudfront stop_stack_set_operation
# stop_iot
# change_waf change waf to free edition
 
import json
import simple_notification  
import traceback

import get_list_of_possible_resources
import stop_autoscaling
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

def	lambda_handler(event, context):

	RunningInstances =	[]
	instanceList = ''

	try: 
		# only in play when a list of clients is wanted. 
		# get_list_of_possible_resources.fail_with_list('?')
		stop_autoscaling.suspend_processes('autoscaling',	RunningInstances)
		stop_ecs.stop_instances('ecs',	RunningInstances) # Stop: load balancers
		stop_eks.delete_clusters('eks',	RunningInstances) # Stop: Amazon Elastic Container Service for Kubernetes CreateOperation
		stop_ec2.stop_instances('ec2',	RunningInstances)
		stop_nat_gateway.delete_ec2_nat_gateways('ec2',	RunningInstances) # Stop: Amazon Elastic Compute Cloud NatGateway
		stop_sagemaker.stop_jobs('sagemaker', RunningInstances)
		stop_robomaker.stop_jobs('robomaker',RunningInstances)
		stop_rds.stop_instances('rds',RunningInstances)
		stop_rds.autostart_instances('rds',RunningInstances)
		stop_rds.stop_clusters('rds',RunningInstances)
		stop_rds.autostart_clusters('rds',RunningInstances)
		stop_rds.stop_clusters('docdb',RunningInstances) # stop docdb - same logic as rds cluster
		stop_dax.delete_clusters('dax',RunningInstances)
		stop_emr.stop_clusters('emr',RunningInstances)
		stop_kinesis.delete_streams('kinesis',RunningInstances)	
		stop_kinesisanalytics.stop_applications('kinesisanalytics',RunningInstances)	
		stop_elasticache.delete_clusters('elasticache',	RunningInstances)
		stop_glue.stop_jobs('glue',	RunningInstances)
		stop_elastisearch.delete_domains('es',	RunningInstances)
		stop_dms.delete_instances('dms',	RunningInstances)
		stop_redshift.change_to_smallest('redshift',	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
		# stop_redshift.delete_cluster('redshift',	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
		#	stop_iot_stop_all('iot',	RunningInstances)	
		if	len(RunningInstances) >	0:
			instanceList = json.dumps(RunningInstances)
			simple_notification.send_info(instanceList)
	except Exception as exception:
		if	len(RunningInstances) >	0:
			instanceList = json.dumps(RunningInstances)
		simple_notification.send_info(instanceList + ' - exception ' + traceback.format_exc() )
		raise exception 
		
	return	{
		"statusCode":	200,
		"body": instanceList 
	}


