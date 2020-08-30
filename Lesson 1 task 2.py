import requests
import json

key = 'AIzaSyCjxnoyE5bPDeiOU7cxdre0QsZ5bEQE5jI'
channel_key = 'UCcvMdU6a3jqWxBd3ODJS4CQ'
#request 1
url = 'https://www.googleapis.com/youtube/v3/channelSections'

param = {'part': 'contentDetails',
         'channelId': channel_key,
         'key': key}

r = requests.get(url, param)

if r.ok:
    j_data = r.json()

    with open('json_channeldetails.txt', 'w') as f:
        json.dump(j_data, f, ensure_ascii=False)
else:
    print(f'Error with code: {r.status_code}')

url = 'https://www.googleapis.com/youtube/v3/channels'
#request 2
param = {'part': 'contentDetails',
         'id': channel_key,
         'key': key}

r = requests.get(url, param)
if r.ok:
    j_data = r.json()

    with open('json_channels.txt', 'w') as f:
        json.dump(j_data, f, ensure_ascii=False)
else:
    print(f'Error with code {url} : {r.status_code}')