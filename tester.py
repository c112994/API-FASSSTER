import http.client
import json
from collections import *
import re

def gender(month, year):
	actual_data = connect(month,year)

	barangays = set([i['barangay'] for i in actual_data])

	# Build the dictionary
	d = {}
	for brgy in barangays:
		d[brgy] = {}
		d[brgy]['Underweight'] = 0
		d[brgy]['Normal'] = 0
		d[brgy]['Overweight'] = 0
		d[brgy]['Obese'] = 0
	out = {}
	for i,row in enumerate(actual_data):
		num_w = re.findall('\d+', row['weight'])
		num_h = re.findall('\d+', row['height'])
		if (len(num_w)*len(num_h) >= 1):
			w = float(num_w[0])
			h = float(num_h[0])/100
			if (h*w) >= 1:
				out[str(i)] = {}		
				bmi = w/(h*h)
				out[str(i)] = {'Barangay' : row['barangay'], 'Age' : row['age_consulted'], 'Height' : h, 'Weight' : w, 'BMI' : ("%.2f" % bmi)}
				if bmi < 18.5: d[row['barangay']]['Underweight'] += 1
				elif bmi >= 18.5 and bmi < 25: d[row['barangay']]['Normal'] += 1
				elif bmi >= 25 and bmi < 30: d[row['barangay']]['Overweight'] += 1
				else: d[row['barangay']]['Obese'] += 1
	print(d)

def connect(month, year):
	conn = http.client.HTTPConnection("10.11.82.25")

	headers = {
	    'shinekey': "3670407151512120101064700",
	    'shinesecret': "3670407151512120101064700",
	    'cache-control': "no-cache"
	    }

	conn.request("GET", "/devemr/api/fassster/getall?month={0}&year={1}".format(month,year), headers=headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)
	actual_data = data['data']
	return actual_data

gender(8,2016)