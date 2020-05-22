# -*- coding: utf-8 -*-
import os, requests, uuid, json, string

key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

path = '/translate?api-version=3.0'
language = '&to=de'
params = language
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
text = 'hello'
text = text.replace('\n','')
body = [{
    'text': text
}]

request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

json_string = json.dumps(response, sort_keys=True, indent=4,
                 ensure_ascii=False, separators=(',', ': '))
json_string = json_string.encode('utf-8')
print(json_string)
