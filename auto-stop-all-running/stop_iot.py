# File_name: stop_iot.py
# Purpose: Stop iot that are running.
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
# instance_type = 'glue'
def stop_jobs(instance_type,RunningInstances) : 
	client = boto3.client(instance_type)

	crawlers = client.get_crawlers()['Crawlers'] 
	for crawler in crawlers:
		if crawler['State'] == 'RUNNING' :	
			RunningInstances.append(instance_type + ' crawler running	' + crawler['Name'])
			print(crawler['State'] + ' crawler ' + crawler['Name'])
			response = client.stop_crawler( Name=crawler['Name'] )
		if crawler['State'] == 'SCHEDULED' :	
			RunningInstances.append(instance_type + ' crawler running	' + crawler['Name'])
			print(crawler['State'] + ' crawler ' + crawler['Name'])
			response = client.stop_crawler_schedule( Name=crawler['Name'] )
		
	jobs = client.get_jobs( )['Jobs']
	for job in jobs:
		job_runs = client.get_job_runs( JobName=job['Name'] )['JobRuns']
		for job_run in job_runs:
			if job_run['JobRunState'] == 'RUNNING' :	
				RunningInstances.append(instance_type + ' Job 	' + job_id)
				print(status_value + ' Job ' + job_name)
				client.batch_stop_job_run( JobName=job['Name'] )
				break

	triggers = client.get_triggers( )['Triggers']
	for trigger in triggers:
		if trigger['State'] in ['CREATING','CREATED','ACTIVATING','ACTIVATED','UPDATING'] :	
			trigger_name = trigger['Name']
			RunningInstances.append(instance_type + ' trigger	' + trigger['State'] + '	' + trigger_name)
			print(status_value + ' Unable to stop Job ' + job_name);
			response = client.stop_trigger( Name=trigger_name )

	return

list_active_violations()
list_attached_policies()
list_audit_findings()
list_audit_tasks()
list_authorizers()
list_billing_groups()
list_ca_certificates()
list_certificates()
list_certificates_by_ca()
list_indices()
list_job_executions_for_job()
list_job_executions_for_thing()
list_jobs()
list_ota_updates()
list_outgoing_certificates()
list_policies()
list_policy_principals()
list_policy_versions()
list_principal_policies()
list_principal_things()
list_role_aliases()
list_scheduled_audits()
list_security_profiles()
list_security_profiles_for_target()
list_streams()
list_tags_for_resource()
list_targets_for_policy()
list_targets_for_security_profile()
list_thing_groups()
list_thing_groups_for_thing()
list_thing_principals()
list_thing_registration_task_reports()
list_thing_registration_tasks()
list_thing_types()
list_things()
list_things_in_billing_group()
list_things_in_thing_group()
list_topic_rules()
list_v2_logging_levels()
list_violation_events()


delete_account_audit_configuration()
delete_authorizer()
delete_billing_group()
delete_ca_certificate()
delete_certificate()
delete_dynamic_thing_group()
delete_job()
delete_job_execution()
delete_ota_update()
delete_policy()
delete_policy_version()
delete_registration_code()
delete_role_alias()
delete_scheduled_audit()
delete_security_profile()
delete_stream()
delete_thing()
delete_thing_group()
delete_thing_type()
delete_topic_rule()
delete_v2_logging_level()

