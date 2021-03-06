# File_name: stop_glue.py
# Purpose: Stop crawlers, jobs that are running. And stop triggers that are active
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import boto3
 
# instance_type = 'glue'
def stop_jobs(instance_type,region_name_,RunningInstances) : 
	client = boto3.client(instance_type, region_name=region_name_)

	crawlers = client.get_crawlers()['Crawlers'] 
	for crawler in crawlers:
		if crawler['State'] == 'RUNNING' :	
			RunningInstances.append(instance_type + ' crawler running	' + crawler['Name'])
			print(crawler['State'] + '	'	+ region_name_ + ' crawler ' + crawler['Name'])
			response = client.stop_crawler( Name=crawler['Name'] )
		if crawler['State'] == 'SCHEDULED' :	
			RunningInstances.append(instance_type + ' crawler running	' + crawler['Name'])
			print(crawler['State'] + '	'	+ region_name_ + ' crawler ' + crawler['Name'])
			response = client.stop_crawler_schedule( Name=crawler['Name'] )
		
	jobs = client.get_jobs( )['Jobs']
	for job in jobs:
		job_runs = client.get_job_runs( JobName=job['Name'] )['JobRuns']
		for job_run in job_runs:
			if job_run['JobRunState'] == 'RUNNING' :	
				RunningInstances.append(instance_type + '	'	+ region_name_ + ' Job 	' + job_id)
				print(status_value + '	'	+ region_name_ + ' Job ' + job_name)
				client.batch_stop_job_run( JobName=job['Name'] )
				break

	triggers = client.get_triggers( )['Triggers']
	for trigger in triggers:
		if trigger['State'] in ['CREATING','CREATED','ACTIVATING','ACTIVATED','UPDATING'] :	
			trigger_name = trigger['Name']
			RunningInstances.append(instance_type + '	'	+ region_name_ + ' trigger	' + trigger['State'] + '	' + trigger_name)
			print(status_value + '	'	+ region_name_ + ' trigger ' + trigger_name);
			response = client.stop_trigger( Name=trigger_name )

	return



