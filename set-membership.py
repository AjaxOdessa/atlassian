#!/usr/bin/env python3
import csv
import json
import requests
import sys
import urllib.parse

base_url = ''
login = ''
password = ''

if len(sys.argv) != 2:
	print('Script require single parameter - CSV file, where each line is a single "name, group" record.')
	sys.exit(1)
else:
	infile = sys.argv[1]
headers = { 'Content-Type': "application/json", 'Accept': "application/json", 'Cache-Control': "no-cache" }

def get_cookie(base, username, password):
	getCookie = requests.post(url=base + '/rest/auth/1/session', data='{ "username": "' + username + '", "password": "' + password + '" }', headers={'Content-Type': 'application/json'})
	if (getCookie.status_code == 200):
		result = {}
		payload = json.loads(getCookie.content.decode('utf8'))
		for i in payload:
			result['Cookie'] = payload['session']['name'] + '=' + payload['session']['value']
		return result
	else:
		return getCookie

def dump_request_errors(req):
	response = json.loads(req.content.decode('utf8'))
	for m in response['errorMessages']:
		print(m)

authCookie = get_cookie(base_url, login, password)
if not isinstance(authCookie, dict):
	dump_request_errors(authCookie)
	sys.exit(1)
else:
	headers.update(authCookie)

with open(infile, 'r', newline='') as csvfile:
	for line in csv.reader(csvfile, delimiter = ','):
		rest_api = base_url + '/rest/api/2/group/user'
		request = requests.post(rest_api, params={"groupname":urllib.parse.quote(line[1])}, json={"name":line[0]}, headers=headers)
		if request.status_code == 201:
			print("Successfully added user '" + line[0] + "' to group '" + line[1] + "'")
		elif request.status_code in (400, 404):
			dump_request_errors(request)
		else:
			dump_request_errors(request)
			sys.exit(1)
