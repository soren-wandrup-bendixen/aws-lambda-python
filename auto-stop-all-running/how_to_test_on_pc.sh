
python3 <<EOF
import lambda_function
context = []
event = []
lambda_function.lambda_handler(event,context)
quit() 
EOF
