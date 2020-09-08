
python3 <<EOF
import lambda_function
context = []
event = { \
  "status": "Success", \
  "images": [ \
    { \
      "s3_image_file_base_name": "bbd3207c.png", \
      "s3_image_file_path": "images/", \
      "s3_bucket_name": "gole-images", \
      "etag": "1", \
      "mime_type": "image/jpeg", \
      "one": "1", \
      "two": "2", \
      "three": "3", \
      "mainfigure": "", \
      "season": "", \
      "size": "", \
      "environment": "" \
    } \
  ] \
}
lambda_function.lambda_handler(event,context)
quit()
EOF


