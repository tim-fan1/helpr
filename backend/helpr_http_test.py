'''
HTTP API integration tests for the end-to-end functionality of the helpr application
'''

import config
import requests
import json

BASE_URL=f"http://127.0.0.1:{config.PORT}"

def test_make_single_request():
    """
    one student make single request.
    ensure '/queue' route gives correct response.
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    response = requests.get(f"{BASE_URL}/queue")
    assert response.status_code == 200
    assert json.loads(response.text) == [{'zid':'z1234567','description':'help','status':'waiting'}]

def test_two_student_make_two_request():
    """
    two students each make one request.
    ensure '/queue' route gives correct response.
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    response = requests.get(f"{BASE_URL}/queue")
    assert response.status_code == 200
    assert json.loads(response.text) == [{'zid':'z1234567','description':'help','status':'waiting'},
                                         {'zid':'z7654321','description':'HELP','status':'waiting'}]

def test_one_student_make_two_request():
    """
    one student make two requests.
    expects BadRequest to be raised in response.
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    response = requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'HELP'})
    assert response.status_code == 400

def test_three_student_make_three_request():
    """
    three students make one request each.
    third student to make request should be in position 2 in the queue (3rd in the queue).
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    response = requests.get(f"{BASE_URL}/remaining",params={'zid':'z5258270'})
    assert response.status_code == 200
    assert json.loads(response.text) == {'remaining':2}

def test_four_student_make_four_request():
    """
    four students make one request each.
    third student to make request should be in position 2 in the queue (3rd in the queue).
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})
    response = requests.get(f"{BASE_URL}/remaining",params={'zid':'z5258270'})
    assert response.status_code == 200
    assert json.loads(response.text) == {'remaining':2}

def test_four_student_make_four_request_one_resolved():
    """
    four students make one request each.
    second student's request is set to receiving, then resolved.
    third student to make request should be in position 1 in the queue (2nd in the queue).
    """
    requests.delete(f"{BASE_URL}/end")
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z7654321'})
    response = requests.get(f"{BASE_URL}/remaining",params={'zid':'z5258270'})
    assert response.status_code == 200
    assert json.loads(response.text) == {'remaining':1}

def test_four_student_make_multiple_requests_reprioritise():
    """
    four students make one request each.
    first three students requests are resolved. (fourth request cancelled).
    
    first three students make one request each.
    first two students requests are resolved. (third request cancelled).

    first two students make one request each.
    first student's request is resolved. (second request cancelled).

    all four students make request.
    set third student to be receiving for fun.
    when queue is reprioritized,
    last student needs help the most. then second-last, third-last, and first student.
    """
    requests.delete(f"{BASE_URL}/end")
    # four students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})
    # first three resolved. fourth one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z7654321'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z5258270'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z5258270'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z5258271'})
    # first three students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    # first two resolved. third one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z5258270'})
    # first two students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    # first one resolved. second one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z7654321'})

    # make four requests again.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})

    # set one request to be receiving for fun.
    requests.post(f"{BASE_URL}/help", json={'zid':'z5258270'})

    # reprioritise queue.
    requests.post(f"{BASE_URL}/reprioritise")
    response = requests.get(f"{BASE_URL}/queue")
    assert response.status_code == 200
    assert json.loads(response.text) == [{'zid':'z5258271','description':'heLP','status':'waiting'},
                                         {'zid':'z5258270','description':'heLp','status':'receiving'},
                                         {'zid':'z7654321','description':'HELP','status':'waiting'},
                                         {'zid':'z1234567','description':'help','status':'waiting'}]

    response = requests.get(f"{BASE_URL}/remaining",params={'zid':'z7654321'})
    assert response.status_code == 200
    assert json.loads(response.text) == {'remaining':1}

def test_four_student_make_multiple_requests_reprioritise_revert():
    """
    four students make one request each.
    first three students requests are resolved. (fourth request cancelled).
    
    first three students make one request each.
    first two students requests are resolved. (third request cancelled).

    first two students make one request each.
    first student's request is resolved. (second request cancelled).

    all four students make request.
    set third student to be receiving for fun.
    reset (**revert**) third student to be waiting.
    when queue is reprioritized,
    last student needs help the most. then second-last, third-last, and first student.
    """
    requests.delete(f"{BASE_URL}/end")
    # four students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})
    # first three resolved. fourth one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z7654321'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z5258270'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z5258270'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z5258271'})
    # first three students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    # first two resolved. third one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.post(f"{BASE_URL}/help", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z7654321'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z5258270'})
    # first two students make one request each.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    # first one resolved. second one cancelled.
    requests.post(f"{BASE_URL}/help", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/resolve", json={'zid':'z1234567'})
    requests.delete(f"{BASE_URL}/cancel", json={'zid':'z7654321'})

    # make four requests again.
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z1234567','description':'help'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z7654321','description':'HELP'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258270','description':'heLp'})
    requests.post(f"{BASE_URL}/make_request", json={'zid':'z5258271','description':'heLP'})

    # set one request to be receiving for fun.
    requests.post(f"{BASE_URL}/help", json={'zid':'z5258270'})
    # revert request to be waiting.
    requests.post(f"{BASE_URL}/revert", json={'zid':'z5258270'})

    # reprioritise queue.
    requests.post(f"{BASE_URL}/reprioritise")
    response = requests.get(f"{BASE_URL}/queue")
    assert response.status_code == 200
    assert json.loads(response.text) == [{'zid':'z5258271','description':'heLP','status':'waiting'},
                                         {'zid':'z5258270','description':'heLp','status':'waiting'},
                                         {'zid':'z7654321','description':'HELP','status':'waiting'},
                                         {'zid':'z1234567','description':'help','status':'waiting'}]

    response = requests.get(f"{BASE_URL}/remaining",params={'zid':'z7654321'})
    assert response.status_code == 200
    assert json.loads(response.text) == {'remaining':2}
