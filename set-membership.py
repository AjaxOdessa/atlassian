#!/usr/bin/env python3
import csv
import json
import requests
import sys

base_url = ''
login = ''
password = ''

if len(sys.argv) != 2:
	print('Script require single parameter - CSV file, where each line is a single "name, group" record.')
	print('CSV dump can be produced with the next SQL request (example provided for Postgres):')
	print("\COPY (SELECT child_name, parent_name FROM cwd_membership ORDER BY 2,1) TO '/tmp/membership.csv' WITH CSV QUOTE '\"' DELIMITER ',';")
	print('or')
	print("\COPY (SELECT DISTINCT u.user_name, g.group_name FROM cwd_user u JOIN cwd_membership m ON u.id = m.child_id JOIN cwd_group g ON m.parent_id = g.id WHERE g.group_name NOT IN ('_licensed-jira', '_licensed-confluence', '_licensed-bamboo', '_licensed-fecru', 'system-administrators', 'confluence-administrators') AND u.active = 1 ORDER BY 2,1) TO '/tmp/temp.csv' WITH CSV QUOTE '\"' DELIMITER ',';")
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
		request = requests.post(rest_api, params={"groupname":line[1]}, json={"name":line[0]}, headers=headers)
		if request.status_code == 201:
			print("Successfully added user '" + line[0] + "' to group '" + line[1] + "'")
		elif request.status_code in (400, 404):
			dump_request_errors(request)
		else:
			dump_request_errors(request)
			sys.exit(1)
