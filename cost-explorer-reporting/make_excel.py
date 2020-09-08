# File_name: make_excel.py
# Purpose: take cost_usage_response and turn that into a pandas.dataframe plus generate an excel sheet with details, pivot and graph.  
# Problem: 
# Author: Søren Wandrup-Bendixen
# Email: soren.wandrup-Bendixen@cybercom.com
# Created: 2019-09-11
# Called from lambda_handler.py

import pandas
import xlsxwriter
import numpy
import os
import io
import datetime


def make_detail_dataframe ( cost_usage_response ):
	# Create a Pandas dataframe from some data.
	# df = pandas.DataFrame.from_dict(cost_usage_response)
	rows = [] 
	for usage_interval_keys in cost_usage_response :
		# start and end date
		for usage_key in usage_interval_keys['Groups'] :
			if float(usage_key['Metrics']['UnblendedCost']['Amount']) > 0.002 : # has to be more than 0.2 cents per day!
				row = { 
			  		  'start date': pandas.to_datetime(arg=usage_interval_keys['TimePeriod']['Start'], format= '%Y-%m-%d')
#					, 'end date':usage_interval_ke,ys['TimePeriod']['End']
					, 'usage type':usage_key['Keys'][0]
					, 'amount value': float(usage_key['Metrics']['UnblendedCost']['Amount'])
					, 'amount curre#ncy': usage_key['Metrics']['UnblendedCost']['Unit']
				}
				rows.append(row)
	dataFrame = pandas.DataFrame(rows)
	return dataFrame

def create_excel_file_in_memory ( dataFrame ):
	# Create a Pandas Excel writer using XlsxWriter as the egine.
	output = io.BytesIO()
	writer = pandas.ExcelWriter(output, engine='xlsxwriter', date_format='YYYY-MM-DD', datetime_format='YYYY-MM-DD')
	# Convert the dataframe to an XlsxWriter Excel object.
	dataFrame.to_excel(writer, sheet_name='Details')

	# Now make the pivot table on top of the details
	pivotDataFrame = dataFrame[['start date','usage type','amount value']]
	pivot = pandas.pivot_table(
		  pivotDataFrame	
		, index=['start date']
		, columns=['usage type']
		, values=['amount value']
		, aggfunc=numpy.sum
	)
	pivot.to_excel(writer, sheet_name='Pivot')

	# Now make the stacked chart using the pivot table 
	workbook = writer.book
	worksheet = workbook.add_worksheet('StackedChart')
	# Create a chart object.
	chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
	for column in range(1,pivot.shape[1]):
		#     [sheetname, first_row, first_col, last_row, last_col]
		# pivot.shape[0] is number of rows, while pivot.shape[1] is number of columns
		chart.add_series({
			'name':       ['Pivot', 1, column],
			'categories': ['Pivot', 4, 0, pivot.shape[0]-1, 0],
			'values':     ['Pivot', 4, column, pivot.shape[0]-1, column]
			})
	chart.set_x_axis({'date_axis': True, 'num_format': 'YYYY-MM-DD' })
	worksheet.insert_chart('A1', chart, {'x_scale': 3.0, 'y_scale': 3.0})
	# Freeze the panes of the pivot table
	worksheet = workbook.get_worksheet_by_name('Pivot')
	worksheet.set_column(0, 0, 12) # Set Column start_date to width 12
	worksheet.freeze_panes('B3')
	worksheet.autofilter(1,0,pivot.shape[0]-1,pivot.shape[1]-1)

	# Close the Pandas Excel writer and output the Excel file.
	writer.save()	
	return output
