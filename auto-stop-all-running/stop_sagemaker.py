# File_name: stop_sagemaker.py
# Purpose: Stop	SageMaker that are running
# Problem: botocore.exceptions.ClientError: An error occurred (UnknownOperationException) when calling the ListCompilationJobs operation: The requested operation is not supported in the called region.
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
from botocore.exceptions import ClientError

# instance_type	= 'sagemaker'
def	stop_jobs(instance_type,region_name_,RunningInstances) :	
	client	= boto3.client(instance_type, region_name=region_name_)

	# *** stop_training_job that are running
	jobs =	client.list_training_jobs( StatusEquals='InProgress' )['TrainingJobSummaries']
	for job in	jobs:
		job_name = job['TrainingJobName']
		RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	TrainingJobName	   ' + job_name)
		response = client.stop_training_job( TrainingJobName=job_name	)
		
	# *** stop_compilation_job	that are running
	try:
		jobs =	client.list_compilation_jobs( StatusEquals='INPROGRESS'	)['CompilationJobSummaries']
		for job in	jobs:
			job_name = job['CompilationJobName']
			RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	CompilationJobName	  ' + job_name)
			response = client.stop_compilation_job( CompilationJobName=job_name )
	except ClientError as exception:
		if ( exception.response['Error']['Code'] == 'UnknownOperationException' and 'The requested operation is not supported in the called region.' in exception.response['Error']['Message'] ) or exception.response['Error']['Code'] in ['InternalFailure','AccessDeniedException'] :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support CompilationJobSummaries	' )
		else:
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support CompilationJobSummaries	' + exception.response['Error']['Code'] + '+' + exception.response['Error']['Message']) 
			raise exception
			
	# *** stop_hyper_parameter_tuning_job that	are	running
	jobs =	client.list_hyper_parameter_tuning_jobs( StatusEquals='InProgress' )['HyperParameterTuningJobSummaries']
	for job in	jobs:
		job_name = job['HyperParameterTuningJobName']
		RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	HyperParameterTuningJobName	   ' + job_name)
		response = client.stop_hyper_parameter_tuning_job( HyperParameterTuningJobName=job_name )

	# *** stop_labeling_job that are running
	try:
		jobs	= client.list_labeling_jobs( StatusEquals='InProgress' )['LabelingJobSummaryList']
		for job in jobs:
			job_name =	job['LabelingJobName']
			RunningInstances.append(instance_type  + '	'	+ region_name_ + ' LabelingJobName	  ' + job_name)
			response =	client.stop_labeling_job( LabelingJobName=job_name )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'UnknownOperationException' and 'The requested operation is not supported in the called region.' in exception.response['Error']['Message'] :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support LabelingJobSummaryList	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support LabelingJobSummaryList	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception



	# *** stop_transform_job that are running
	try:
		jobs =	client.list_transform_jobs(	StatusEquals='InProgress' )['TransformJobSummaries']
		for job in	jobs:
			job_name = job['TransformJobName']
			RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	TransformJobName	' + job_name)
			response = client.stop_transform_job(	TransformJobName=job_name )
	except ClientError as exception:
		if exception.response['Error']['Code'] == 'UnknownOperationException' and 'The requested operation is not supported in the called region.' in exception.response['Error']['Message'] :
			print ( instance_type	 + '	'	+ region_name_ + '	 does not support TransformJobSummaries	' )
		else:
#			print ( instance_type	 + '	'	+ region_name_ + '	 does not support TransformJobSummaries	' + exception.response['Error']['Code'] + exception.response['Error']['Message']) 
			raise exception



	# *** stop_notebook_instance that are running
	jobs =	client.list_notebook_instances(	StatusEquals='InService' )['NotebookInstances']
	for job in	jobs:
		job_name = job['NotebookInstanceName']
		RunningInstances.append(instance_type	 + '	'	+ region_name_ + '	NotebookInstanceName	' + job_name)
		response = client.stop_notebook_instance(	NotebookInstanceName=job_name )

	return
