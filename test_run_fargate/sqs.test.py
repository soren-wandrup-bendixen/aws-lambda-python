import json

def lambda_handler(event, context):
	# TODO implement
	sqs = boto3.client('sqs')
	sqs_json = { 
		  "message-type":"tar-extract-image"
		, "bucket":"bucket"
		, "key":"key"
		, "image":"image"
		, "image_member_name":"image_member_name"
	}
	sqs.send_message(QueueUrl=os.environ['SqsUrl'], MessageBody=json.dumps(sqs_json) )
	return {
		'statusCode': 200,
		'body': json.dumps('Hello from Lambda!')
	}
