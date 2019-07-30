# File_name: lambda_handler.py
# Purpose: Lambda function to stop all aws services	that cost money	in dev and test
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from CloudWatch event rule	scheduled :	cron( 0	18,19 ? * * * ) 
# Total time to run per execution is 10 minutes. And is set to run twice a day. 

# To be developed
# stop_iot
# stop_neptune
# stop_batch - 
# stop_sdb - simpledb - will delete the domain calling delete_domain
# stop_cloudfront stop_stack_set_operation
# change_waf change waf to free edition

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

def	lambda_handler(event, context):

	RunningInstances =	[]
	instanceList = ''

	try: 
		# only in play when a list of clients is wanted. 
		# get_list_of_possible_resources.fail_with_list('?')
		region_names = all_region_names.get_list('ec2')
		# for simple testing; region_names = ['us-east-1']
		for region_name_ in region_names:
			print (region_name_ + ' time:	' + str(datetime.datetime.now()))
			stop_autoscaling.suspend_processes('autoscaling', region_name_, RunningInstances)
			stop_emr.stop_clusters('emr', region_name_, RunningInstances) # Stop EMR before ec2's otherwise the ec2 of emr will be terminated individually
			stop_elb.delete_instances('elb', region_name_,	RunningInstances) # Delete load balancers
			stop_elb.delete_instances('elbv2', region_name_,	RunningInstances) # Delete load balancers
			stop_ecs.stop_instances('ecs', region_name_,	RunningInstances) # Stop: Amazon Elastic Container Service (ECS)
			stop_eks.delete_clusters('eks', region_name_,	RunningInstances) # Stop: Amazon Elastic Container Service for Kubernetes CreateOperation
			stop_ec2.stop_instances('ec2', region_name_,	RunningInstances)
			stop_nat_gateway.delete_ec2_nat_gateways('ec2', region_name_,	RunningInstances) # Stop: Amazon Elastic Compute Cloud NatGateway
			stop_sagemaker.stop_jobs('sagemaker', region_name_, RunningInstances)
			stop_robomaker.stop_jobs('robomaker', region_name_, RunningInstances)
			stop_rds.stop_instances('rds', region_name_, RunningInstances)
			stop_rds.autostart_instances('rds', region_name_, RunningInstances)
			stop_rds.stop_clusters('rds', region_name_, RunningInstances)
			stop_rds.autostart_clusters('rds', region_name_, RunningInstances)
			stop_rds.stop_clusters('docdb', region_name_, RunningInstances) # stop docdb - same logic as rds cluster
			stop_dax.delete_clusters('dax', region_name_, RunningInstances)
			stop_kinesis.delete_streams('kinesis', region_name_, RunningInstances)	
			stop_kinesisanalytics.stop_applications('kinesisanalytics', region_name_, RunningInstances)	
			stop_elasticache.delete_clusters('elasticache', region_name_,	RunningInstances)
			stop_glue.stop_jobs('glue', region_name_,	RunningInstances)
			stop_elastisearch.delete_domains('es', region_name_,	RunningInstances)
			stop_dms.delete_instances('dms', region_name_,	RunningInstances)
			stop_redshift.change_to_smallest('redshift', region_name_,	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
			# stop_redshift.delete_cluster('redshift', region_name_,	RunningInstances) # As I see it either I have to delete the cluster or turn it into a single-node cluster. Cant just stop it.
			#	stop_iot_stop_all('iot', region_name_,	RunningInstances)	
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


