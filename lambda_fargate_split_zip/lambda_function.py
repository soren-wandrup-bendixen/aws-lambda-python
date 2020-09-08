import boto3
def lambda_handler(event,context):
	client = boto3.client('ecs')
#	print(client.list_clusters())
	response = client.run_task(
		cluster='python-fargate-cluster', # name of the cluster
		launchType = 'FARGATE',
		taskDefinition='fargate-task-definition:2', # replace with your task definition name and revision
		count = 1,
		platformVersion='LATEST',
		networkConfiguration={
			'awsvpcConfiguration': {
				'subnets': [
					'subnet-59e7cb13', # replace with your public subnet or a private with NAT
					'subnet-5bb92275' # Second is optional, but good idea to have two
				],
				'assignPublicIp': 'ENABLED'
			}
		}
		, overrides={
			'containerOverrides': [
				{
					'name': 'fargate_split_container'		
					, 'environment': [
						{
							'name': 'Command'
							, 'value': json.dumps(event)
						}
					]
				}
			]  
		}
	)
	return str(response)
