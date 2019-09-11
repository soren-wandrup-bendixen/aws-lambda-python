rm -f -R numpys* 
rm -f -R pandas*
cp -r ../pc_numpy/* .
cp -r ../pc_pandas/* .
export TOPIC_ARN='arn:aws:sns:us-east-1:015670528421:cost-explorer-sns-topic'
export S3_BUCKET='soren-personalize-test'
python3 <<EOF
import lambda_function
context = []
event = []
lambda_function.lambda_handler(event,context)
quit()
EOF
