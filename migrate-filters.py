#!/usr/bin/env python3

import datetime
import json
import requests

def requestGet(args):
	result = requests.get(url=args[0], data=args[1], headers=args[2])
	return result

def requestPost(args):
	result = requests.post(url=args[0], data=args[1], headers=args[2])
	return result

def get_cookie(base,username,password):
	getCookie = requestPost([base + '/rest/auth/1/session','{ "username": "' + username + '", "password": "' + password + '" }',{'Content-Type': 'application/json'}])
	if (getCookie.status_code == 200):
		result = {}
		payload = json.loads(getCookie.content.decode('utf8'))
		for i in payload:
			result['Cookie'] = payload['session']['name'] + '=' + payload['session']['value']
		return result
	else:
		return getCookie.status_code

def timestamp(message):
	now = datetime.datetime.now()
	print('[' + str(now) + '] ' + message)

src_login = "SRC. Username"
src_password = "SRC. Password"
src_jira = "SOURCE JIRA BASE URL"
src_headers = {'Content-Type': 'application/json'}

dst_login = "DEST. Username"
dst_password = "DEST. Password"
dst_jira = "DESTINATION JIRA BASE URL"
dst_headers = {'Content-Type': 'application/json'}

src_authCookie = get_cookie(src_jira, src_login, src_password)
if (src_authCookie == 401):
	print("Getting source authentication has failed.")
	sys.exit(1)
else:
	src_headers.update(src_authCookie)

dst_authCookie = get_cookie(dst_jira, dst_login, dst_password)
if (dst_authCookie == 401):
	print("Getting destination authentication has failed.")
	sys.exit(1)
else:
	dst_headers.update(dst_authCookie)

timestamp("Started.")

src_filters = json.loads(requestGet([src_jira + '/rest/api/2/filter/my', '', src_headers]).content.decode('utf8'))

for f in src_filters:
	body = '{ "name": ' + json.dumps(f['name']) + ', "jql": ' + json.dumps(f['jql']) + ' }'
	dst_filter = requestPost([dst_jira + '/rest/api/2/filter', body, dst_headers])
	if (dst_filter.status_code != 200):
		timestamp("Filter with " + body + " body wasn't created successfully, with error")
		timestamp("\t" + str(json.loads(dst_filter.content.decode('utf8'))['errorMessages']))
	else:
		timestamp("Filter " + i['name'] + " was successfully created.")

timestamp("Done.")
