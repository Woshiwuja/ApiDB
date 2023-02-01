#To do
# Make request to get token and put it into a variable
# Check scan id details for each scan
# put data into database 
#
#
#
#
#
#
#
#
#
#

import json
import requests
import psycopg2
from types import SimpleNamespace
import numpy as np


DBNAME = "postgres"
HOST = "localhost"
USER = "postgres"
PASSWORD = "your-super-secret-and-long-postgres-password"
PORT = "5432" 

NESSUS_IP = "10.1.2.41"
NESSUS_PORT = "8834"
NESSUS_USER = "admin"
NESSUS_PASSWORD = "olympos2019"

nessus_base_url = "https://{0}:{1}/".format(NESSUS_IP,NESSUS_PORT)

nessus_creds_json = {'username': 'admin', 'password':'olympos2019'}

#nessus_token = json.loads(requests.post("{}/session".format(nessus_base_url), nessus_creds_json, verify=False).content, object_hook=lambda d:SimpleNamespace(**d)).token

nessus_token = "07c75b46fa3839882575d5a6a0194a30405626e0a8a1fa33"

nessus_headers = {'X-Cookie': 'token= {}'.format(nessus_token)}

#database connection
conn = psycopg2.connect(dbname = DBNAME, host = HOST, user = USER, password = PASSWORD, port = PORT)
conn.autocommit = True

#cursor
cursor = conn.cursor()

#requests 
#get scan list
scan_list = requests.get("{0}scans/".format(nessus_base_url), headers= nessus_headers, verify=False)
print(scan_list.content)
scan_names = list()
#get scan information
#scan_info_by_id = requests.get("{0}scans/{1}".format(nessus_base_url, nessus_scan_id), headers= nessus_headers, verify=False)
#print(scan_info_by_id.content)

#parse json into python object

nessus_scan_list = json.loads(scan_list.content, object_hook=lambda d:SimpleNamespace(**d))
#nessus_scan = json.loads(scan_info_by_id.content, object_hook=lambda d: SimpleNamespace(**d))

#Fill database with scan IDS
scan_ids = np.array([],dtype=int)
for i in range(len(nessus_scan_list.scans)):
    scan_ids = np.append(scan_ids, nessus_scan_list.scans[i].id)
    scan_names.append(str('\''+ nessus_scan_list.scans[i].name + '\''))
    cursor.execute("INSERT INTO nessus_scans(scan_id, scan_name) VALUES ({0},{1}) ON CONFLICT (scan_id) DO NOTHING"
    .format(scan_ids[i],scan_names[i]))
