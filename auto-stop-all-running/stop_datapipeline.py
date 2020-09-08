# File_name: stop_datapipeline.py
# Purpose: Deactivate pipelines that are active
# Problem: 
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-26
# Called from lambda_function.py

import boto3
from botocore.exceptions import EndpointConnectionError

# instance_type	= 'datapipeline'
def	inactivate_pipelines(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		pipelines = client.list_pipelines(  )
		for pipeline in pipelines['pipelineIdList']:
			pipeline_description_list = client.describe_pipelines(pipelineIds=[pipeline['id']])['pipelineDescriptionList']
			fields = pipeline_description_list[0]['fields']
			for field in fields :
				if field['key'] == '@pipelineState' :
					if field['stringValue'] in ['ACTIVE']:
						RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	pipeline	   ' + pipeline['id'])
						response = client.deactivate_pipeline(pipelineId=pipeline['id'], cancelActive=True )
					exit
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_pipelines	' )
	return

def	delete_pipelines(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)
	try:
		pipelines = client.list_pipelines(  )
		for pipeline in pipelines['pipelineIdList']:
			pipeline_description_list = client.describe_pipelines(pipelineIds=[pipeline['id']])['pipelineDescriptionList']
			fields = pipeline_description_list[0]['fields']
			for field in fields :
				if field['key'] == '@pipelineState' :
					if field['stringValue'] in ['PENDING']: 
						RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	activate pipeline	   ' + pipeline['id'])
						response = client.activate_pipeline(pipelineId=pipeline['id'] )
					exit
			RunningInstances.append(instance_type	+ '	'	+ region_name_ + '	delete pipeline	   ' + pipeline['id'])
			response = client.deactivate_pipeline(pipelineId=pipeline['id'], cancelActive=True )
	except EndpointConnectionError as exception:
		print ( instance_type	 + '	'	+ region_name_ + '	 does not support list_pipelines	' )
	return



