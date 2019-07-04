# File_name: stop_sagemaker.py
# Purpose: Stop	SageMaker that are running
# Problem: Amazon boto3	will not list_compilation_jobs and not list_labeling_jobs!
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type	= 'sagemaker'
def	stop_jobs(instance_type,RunningInstances) :	
	client	= boto3.client(instance_type)

	# *** stop_training_job that are running
	jobs =	client.list_training_jobs( StatusEquals='InProgress' )['TrainingJobSummaries']
	for job in	jobs:
		job_name = job['TrainingJobName']
		RunningInstances.append(instance_type	+ '	TrainingJobName	   ' + job_name)
		response = client.stop_training_job( TrainingJobName=job_name	)
		
	# *** stop_compilation_job	that are running
	jobs =	client.list_compilation_jobs( StatusEquals='INPROGRESS'	)['CompilationJobSummaries']
	for job in	jobs:
		job_name = job['CompilationJobName']
		RunningInstances.append(instance_type	+ '	CompilationJobName	  ' + job_name)
		response = client.stop_compilation_job( CompilationJobName=job_name )
	
	# *** stop_hyper_parameter_tuning_job that	are	running
	jobs =	client.list_hyper_parameter_tuning_jobs( StatusEquals='InProgress' )['HyperParameterTuningJobSummaries']
	for job in	jobs:
		job_name = job['HyperParameterTuningJobName']
		RunningInstances.append(instance_type	+ '	HyperParameterTuningJobName	   ' + job_name)
		response = client.stop_hyper_parameter_tuning_job( HyperParameterTuningJobName=job_name )

	# *** stop_labeling_job that are running
	jobs	= client.list_labeling_jobs( StatusEquals='InProgress' )['LabelingJobSummaryList']
	for job in jobs:
		job_name =	job['LabelingJobName']
		RunningInstances.append(instance_type + ' LabelingJobName	  ' + job_name)
		response =	client.stop_labeling_job( LabelingJobName=job_name )

	# *** stop_transform_job that are running
	jobs =	client.list_transform_jobs(	StatusEquals='InProgress' )['TransformJobSummaries']
	for job in	jobs:
		job_name = job['TransformJobName']
		RunningInstances.append(instance_type	+ '	TransformJobName	' + job_name)
		response = client.stop_transform_job(	TransformJobName=job_name )

	# *** stop_notebook_instance that are running
	jobs =	client.list_notebook_instances(	StatusEquals='InService' )['NotebookInstances']
	for job in	jobs:
		job_name = job['NotebookInstanceName']
		RunningInstances.append(instance_type	+ '	NotebookInstanceName	' + job_name)
		response = client.stop_notebook_instance(	NotebookInstanceName=job_name )

	return
