export TOPIC_ARN='arn:aws:sns:us-east-1:015670528421:auto_stop_all'
python3 <<EOF
import lambda_function
context = []
event = { "region_set" : 1 }
lambda_function.lambda_handler(event,context)
quit()
EOF

python3 <<EOF
import lambda_function
context = []
event = { "region_set" : 2 }
lambda_function.lambda_handler(event,context)
quit()
EOF

