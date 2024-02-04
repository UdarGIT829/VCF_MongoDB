import requests
import json

url = "http://127.0.0.1:5000/query"
query_parameters = {
    'do mutation':"true", 
    'query':json.dumps({'_id': 'HG00097'})
    }  

response = requests.get(url, params=query_parameters)

if response.status_code == 200:
    print("Response content:")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
