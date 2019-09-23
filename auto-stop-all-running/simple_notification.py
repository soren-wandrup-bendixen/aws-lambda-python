# File_name: simple_notification.py
# Purpose: Send list of instances/jobs that were running and are now stopped
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-07-01
# Called from lambda_function.py

import os
import boto3
 
def send_info ( message = 'test'):
	# Create an SNS client
	sns = boto3.client('sns')
	topic_arn = os.environ['TOPIC_ARN']
# 'arn:aws:sns:us-east-1:015670528421:auto_stop_all'
	# Publish a simple message to the specified SNS topic
	response = sns.publish(
		TopicArn=topic_arn,    
		Message=message    
	)

	return response
