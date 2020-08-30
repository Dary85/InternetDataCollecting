import requests
import json

username = input('Enter username: ')

params = {'type': 'all'}

url = 'https://api.github.com/users/' + username + '/repos'

responce = requests.get(url, params)

if responce.ok:
    j_data = responce.json()

    with open('json_github.txt', 'w') as f:
        json.dump(j_data, f, ensure_ascii=False)

    for i in range(len(j_data)):
        print(f'Project {i} : {j_data[i]["name"]}')
else:
    print(responce.status_code)
