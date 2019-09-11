# File_name: cost_explorer.py
# Purpose: extract billing information to be able to find out where the cost is too high and find areas to reduce cost
# Problem: botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetCostAndUsage operation: HOURLY data is not publicly supported yet, please reach out to customer service to opt in for private Beta.
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-11
# Called from lambda_handler.py


# Problems: botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetCostAndUsage operation: HOURLY data is not publicly supported yet, please reach out to customer service to opt in for private Beta.
# And has to have special datetime format!
#		      TimePeriod={
#    		      'Start': start_date_.strftime("%Y-%m-%dT%H:%M:%SZ")  # isoformat()
#		        , 'End': end_date_.strftime("%Y-%m-%dT%H:%M:%SZ") # isoformat()
#    		  }


import boto3

def extraxt_full ( start_date_, end_date_, granularity_, filter_ ):
	client = boto3.client('ce')
	# Get the cost from Cost explorer
	# print( start_date_.isoformat())
	response = client.get_cost_and_usage(
		      TimePeriod={
    		      'Start': start_date_.isoformat()
		        , 'End': end_date_.isoformat()
    		  }
    		, Granularity=granularity_
			, Filter=filter_
			, Metrics=['UnblendedCost']
			, GroupBy=[
        		{
            		'Type': 'DIMENSION',
            		'Key': 'SERVICE'
        		},
    		]
	)
	cost_usage_response = response
	while 'nextToken' in response : 
		response = client.get_cost_and_usage(
		      TimePeriod={
    		      'Start': start_date_.isoformat()
		        , 'End': end_date_.isoformat()
    		  }
    		, Granularity=granularity_
			, Filter=filter_
			, Metrics=['UnblendedCost']
			, GroupBy=[
        		{
            		'Type': 'DIMENSION',
            		'Key': 'SERVICE'
        		},
    		]
			, NextPageToken=response['nextToken']
		)
		cost_usage_response.extend(response['ResultsByTime'])
	return cost_usage_response
