# File_name: simple_notification.py
# Purpose: Send list of instances/jobs that were running and are now stopped
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_handler.py

import boto3
 
def send_info ( message = 'test'):
	# Create an SNS client
	sns = boto3.client('sns')

	# Publish a simple message to the specified SNS topic
	response = sns.publish(
		TopicArn='arn:aws:sns:us-east-1:015670528421:auto_stop_all',    
		Message=message    
	)

	return response
