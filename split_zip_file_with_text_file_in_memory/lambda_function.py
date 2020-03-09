# File_name: lambda_function.py
# Purpose: Lambda function to use the event from s3 to get the zip file and split it locally and upload the split files to s3.
# Author: Søren	Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2020-03-04
# Called from s3 event trigger
# Total time to run per execution is 31.26s, Max Memory Used: 279 MB, 1.5 Million rows with a total size of 51.8 MBytes

import io
import boto3
import zipfile
import os
import json
import time

def save_buffer_to_zip_file_in_memory( s3, text_filename_, small_text_file_name_inc_, small_byte_text_line_buffer_, target_bucket_ ): 
	small_text_file_name_ = text_filename_ + "." + str(small_text_file_name_inc_)
	small_zip_file_name_ = text_filename_ + "." + str(small_text_file_name_inc_) + ".zip"
	zip_bytes_io = io.BytesIO()
	zip_archive = zipfile.ZipFile(zip_bytes_io, mode='w',compression=zipfile.ZIP_DEFLATED)
	info = zipfile.ZipInfo(small_text_file_name_)
	info.date_time = time.localtime()
	info.compress_type = zipfile.ZIP_DEFLATED
	# default external_attr is 0600! and that is perfect for now
	# info.external_attr = 0644 << 16L  # -r-wr--r--
	# info.external_attr = 0755 << 16L  # -rwxr-xr-x
	zip_archive.writestr(info, small_byte_text_line_buffer_)
	zip_archive.close()
	zip_bytes_io.seek(0)  # So that bytes are read from beginning
	s3.upload_fileobj(zip_bytes_io, Bucket=target_bucket_, Key=small_zip_file_name_)
	zip_bytes_io.close()

def save_buffer_to_zip_file_on_disk( s3, text_filename_, small_text_file_name_inc_, small_byte_text_line_buffer_, target_bucket_ ): 
	small_text_file_name_ = text_filename_ + "." + str(small_text_file_name_inc_)
	small_zip_file_name_ = text_filename_ + "." + str(small_text_file_name_inc_) + ".zip"
	with open('/tmp/' + small_text_file_name_, 'wb') as out: 
		out.write(small_byte_text_line_buffer_)
	with  zipfile.ZipFile('/tmp/' + small_zip_file_name_, 'w') as myzip:
		myzip.write('/tmp/' + small_text_file_name_)
	response = s3.upload_file	(
		  Filename='/tmp/' + small_zip_file_name_
		, Bucket = target_bucket_
		, Key = small_zip_file_name_
	)
	os.remove('/tmp/' + small_zip_file_name_) ## Delete file when done


def lambda_handler(event, context):
	number_of_slices_ = 6
	# 0. print event
	print(event)
	# 1. Cleanup temp space on disk
	# 2. Get the image info from the event
	s3 = boto3.client('s3')
	for record in event["Records"]:
		target_bucket_ = record["s3"]["bucket"]["name"]
		zip_obj = s3.get_object(Bucket=record["s3"]["bucket"]["name"], Key=record["s3"]["object"]["key"])
		in_buffer_ = io.BytesIO(zip_obj["Body"].read())
		big_zipfile_ = zipfile.ZipFile(in_buffer_)
		print(big_zipfile_.infolist()[0])
		text_filename_ = big_zipfile_.infolist()[0].filename
		compressed_size_ = big_zipfile_.infolist()[0].compress_size
		file_size_ = big_zipfile_.infolist()[0].file_size
		text_file_ = big_zipfile_.open( big_zipfile_.infolist()[0])
		target_small_text_file_size_ = file_size_ / number_of_slices_
		small_text_file_name_inc_ = 0
		small_byte_text_line_buffer_ = bytearray() # empty byte array
		for byte_text_line_ in text_file_:
			if len(small_byte_text_line_buffer_) > target_small_text_file_size_ :
				small_text_file_name_inc_ += 1
				save_buffer_to_zip_file_in_memory( s3, text_filename_, small_text_file_name_inc_, small_byte_text_line_buffer_, target_bucket_ )
				small_byte_text_line_buffer_ = bytearray() # empty byte array
			small_byte_text_line_buffer_ +=  byte_text_line_ # very important to use += to make sure it extends instead of making a new bytearray!
			#print(byte_text_line_)
			#if small_text_file_name_inc_ > 2 : # just during test
			#	break # just during test
		# Now write the last part to the last file	
		small_text_file_name_inc_ += 1
		save_buffer_to_zip_file_in_memory( s3, text_filename_, small_text_file_name_inc_, small_byte_text_line_buffer_, target_bucket_ )
		small_byte_text_line_buffer_ = bytearray() # empty byte array
		in_buffer_.close()		
	return {
		'statusCode': 200,
		'body': json.dumps('All is ok!')
	}
