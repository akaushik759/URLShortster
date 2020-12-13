from printing_data import *

import requests
import json

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

    url_new = 'http://127.0.0.1:5000/'+short_code

    # send request
    resp = requests.get(url_new, headers=headers) 
    resp_body = resp.json()


    assert resp.status_code == 200
    assert resp_body['status'] == 'success'
    assert resp_body['message'] == 'successfully found the original url'

    print_request(resp.request)
    print_response(resp)

def test_with_not_used_short_url():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/ahaa'
    
    # send request
    resp = requests.get(url) 
    resp_body = resp.json()


    assert resp.status_code == 200
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == 'short url not found in database'

    print_request(resp.request)
    print_response(resp)

def test_with_invalid_short_url():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/a'
    
    # send request
    resp = requests.get(url)       

    resp_body = resp.json()


    assert resp.status_code == 400
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == 'invalid short url'

    print_request(resp.request)
    print_response(resp)

def test_with_wrong_method_types():
    test_url = "https://www.apple.com"
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

    url_new = 'http://127.0.0.1:5000/'+short_code

    # send request
    resp1 = requests.post(url_new, headers=headers) 
    resp2 = requests.put(url_new, headers=headers) 
    resp3 = requests.delete(url_new, headers=headers) 
    
    
    # Validate response headers and body contents, e.g. status code.

    assert resp1.status_code == 405
    assert resp2.status_code == 405
    assert resp3.status_code == 405


    print_request(resp1.request)
    print_response(resp1)

    print_request(resp2.request)
    print_response(resp2)

    print_request(resp3.request)
    print_response(resp3)
    