from printing_data import *
from models import *

import requests
import json

'''def test_with_correct_data_no_custom_url():
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

    assert resp.status_code == 201
    assert resp_body['status'] == 'success'
    assert len(resp_body['data']['short_code']) == 6
    assert resp_body['data']['original_url'] == test_url
    assert len(resp_body['data']['unique_id']) != 0
    assert len(resp_body['data']['_id']) != 0

    print_request(resp.request)
    print_response(resp)
    
def test_with_correct_data_custom_url():
    test_url = "https://www.google.com"
    custom_url = 'abcc'
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url,'custom_url': custom_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 201
    assert resp_body['status'] == 'success'
    assert len(resp_body['data']['short_code']) == len(custom_url)
    assert resp_body['data']['original_url'] == test_url
    assert len(resp_body['data']['unique_id']) != 0
    assert len(resp_body['data']['_id']) != 0

    print_request(resp.request)
    print_response(resp)

def test_with_already_used_custom_url():
    test_url = "https://www.google.com"
    custom_url = 'abcc'
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url,'custom_url': custom_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 200
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == "requested custom url is not available"

    print_request(resp.request)
    print_response(resp)

def test_with_short_invalid_custom_url():
    test_url = "https://www.google.com"
    custom_url = 'abc'
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {'original_url': test_url,'custom_url': custom_url}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 422
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == "short url must be greater than or equal to 4 characters"

    print_request(resp.request)
    print_response(resp)

def test_with_empty_payload():
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 422
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == "original url not found in your request"

    print_request(resp.request)
    print_response(resp)

def test_with_empty_original_url_string():
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {"original_url": ""}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 422
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == "original url cannot be empty string"

    print_request(resp.request)
    print_response(resp)

def test_with_original_url_not_string_type():
    url = 'http://127.0.0.1:5000/create'
    
    # Additional headers.
    headers = {'Content-Type':"application/json; charset=utf-8"} 

    # Body
    payload = {"original_url": 3}
    
    # send request
    resp = requests.post(url, headers=headers, data=json.dumps(payload))       
    
    # Validate response headers and body contents, e.g. status code.
    resp_body = resp.json()

    assert resp.status_code == 422
    assert resp_body['status'] == 'error'
    assert resp_body['message'] == "original url needs to be a string"

    print_request(resp.request)
    print_response(resp)'''

def test_with_wrong_method_types():
    test_url = "https://www.google.com"
    url = 'http://127.0.0.1:5000/create'
    
    # Body
    payload = {'original_url': test_url}
    
    # send request
    resp1 = requests.get(url)
    resp2 = requests.put(url)
    resp3 = requests.delete(url)      
    
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