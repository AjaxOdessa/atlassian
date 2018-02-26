#!/usr/bin/env python3
import json
import requests
import sys
import datetime

base_url = ''
login = ''
password = ''
limit = 14
dateTimeFormat = '%d/%b/%y' # https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior

headers = { 'Content-Type': 'application/json', 'Cache-Control': "no-cache" }
addons = requests.get(url=base_url + '/rest/plugins/1.0/', auth=(login, password), headers=headers)
if (addons.status_code == 200):
	addonsResponse = json.loads(addons.content.decode('utf8'))
	for p in addonsResponse['plugins']:
		if (p['usesLicensing'] == True):
			addonLicense = requests.get(url=base_url + p['links']['modify'] + '/license/', auth=(login, password), headers=headers)
			if (addonLicense.status_code == 200):
				addonResponse = json.loads(addonLicense.content.decode('utf8'))
				if ('maintenanceExpiryDateString' in addonResponse.keys()):
					expiration = datetime.datetime.strptime(str(addonResponse['maintenanceExpiryDateString']), dateTimeFormat)
					margin = datetime.datetime.now() + datetime.timedelta(days=limit)
					if (margin > expiration):
						print(p['name'] + ' v' + p['version'] + ' will expire on ' + str(addonResponse['maintenanceExpiryDateString']) + ', which is less that 14 days away!')
					else:
						print(p['name'] + ' v' + p['version'] + ' looks good.')
