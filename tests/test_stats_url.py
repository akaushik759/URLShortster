from printing_data import *

import requests
import json
import time

def test_with_correct_data():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    short_code = resp_body['data']['short_code']
    unique_id = resp_body['data']['unique_id']

    headers['unique_id'] = unique_id

    url_new = 'http://127.0.0.1:5000/'+short_code+'/stats'

    # send request 3 times to redirect url to check if analytics is working
    for i in range(3):
        resp1 = requests.get('http://127.0.0.1:5000/'+short_code) 


    
    resp2 = requests.get(url_new, headers=headers) 
    resp_body = resp2.json()


    assert resp2.status_code == 200
    assert resp_body['status'] == 'success'
    assert resp_body['message'] == 'successfully found the url analytics'
    assert resp_body['data']['count'] > 0

    print_request(resp2.request)
    print_response(resp2)

def test_with_not_created_short_url():
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"}   

    short_code = "abcdef"
    unique_id = "1213"

    headers['unique_id'] = unique_id

    url_new = 'http://127.0.0.1:5000/'+short_code+'/stats'
    
    resp2 = requests.get(url_new, headers=headers) 
    resp_body = resp2.json()


    assert resp2.status_code == 200
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == 'short url not found in database'

    print_request(resp2.request)
    print_response(resp2)

def test_with_wrong_unique_id():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    short_code = resp_body['data']['short_code']
    unique_id = "1234"

    headers['unique_id'] = unique_id

    url_new = 'http://127.0.0.1:5000/'+short_code+'/stats'

    
    resp2 = requests.get(url_new, headers=headers) 
    resp_body = resp2.json()


    assert resp2.status_code == 400
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == 'invalid unique id'

    print_request(resp2.request)
    print_response(resp2)

def test_with_no_unique_id_in_header():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    short_code = resp_body['data']['short_code']
    #unique_id = "1234"

    #headers['unique_id'] = unique_id

    url_new = 'http://127.0.0.1:5000/'+short_code+'/stats'

    
    resp2 = requests.get(url_new, headers=headers) 
    resp_body = resp2.json()


    assert resp2.status_code == 400
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == 'unique id not found in header'

    print_request(resp2.request)
    print_response(resp2)

def test_with_wrong_method_types():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    short_code = resp_body['data']['short_code']
    unique_id = resp_body['data']['unique_id']

    headers['unique_id'] = unique_id

    url_new = 'http://127.0.0.1:5000/'+short_code+'/stats'

    
    resp2 = requests.post(url_new, headers=headers)
    resp3 = requests.put(url_new, headers=headers) 
    resp4 = requests.delete(url_new, headers=headers)  
    


    assert resp2.status_code == 405
    assert resp3.status_code == 405
    assert resp4.status_code == 405

    print_request(resp2.request)
    print_response(resp2)

    print_request(resp3.request)
    print_response(resp2)

    print_request(resp4.request)
    print_response(resp2)