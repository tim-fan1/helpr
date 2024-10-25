'''
Python API unit tests for the core functionality of the helpr application
'''

import pytest

from helpr import make_request, queue, remaining, help, resolve, cancel, revert, reprioritise, end

#################################################
# pytest fixtures.                              #
#################################################

@pytest.fixture(name='student1_problem1')
def fixture_student1_problem1():
    """
    returns (zid1,desc1) tuple fixture.
    """
    return "z1234567","help me"

@pytest.fixture(name='student1_problem2')
def fixture_student1_problem2():
    """
    returns (zid1,desc2) tuple fixture.
    """
    return "z1234567","i am dumb"

@pytest.fixture(name='student1_problem3')
def fixture_student1_problem3():
    """
    returns (zid1,desc2) tuple fixture.
    """
    return "z1234567","big problem"

@pytest.fixture(name='student2_problem1')
def fixture_student2_problem1():
    """
    returns (zid2,desc1) tuple fixture.
    """
    return "z7654321","help me"

@pytest.fixture(name='student2_problem2')
def fixture_student2_problem2():
    """
    returns (zid2,desc2) tuple fixture.
    """
    return "z7654321","i am dumb"

@pytest.fixture(name='student2_problem3')
def fixture_student2_problem3():
    """
    returns (zid2,desc2) tuple fixture.
    """
    return "z7654321","big problem"

@pytest.fixture(name='student1_badproblem1')
def fixture_student1_badproblem1():
    """
    returns (zid1,invaliddesc1) tuple fixture.
    """
    return "z1234567",""

#################################################
# tests make_request(), queue() and end().      #
#################################################

def test_make_no_request():
    """
    no requests made.
    """
    end()
    assert not queue()
    end()
    assert not queue()

def test_one_student_make_one_valid_request(student1_problem1):
    """
    one student makes one valid request.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    end()
    assert not queue()
    
def test_one_student_make_two_valid_request(student1_problem1,student1_problem2):
    """
    one student makes one valid request. 
    the same student then attempts to make another request. 
    the second request will raise a KeyError.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    # there is already a request from student1 in the queue.
    with pytest.raises(KeyError):
        student1,problem2 = student1_problem2
        make_request(student1,problem2)
    end()
    assert not queue()

def test_two_student_make_two_valid_request(student1_problem1,student2_problem1):
    """
    two students each make one valid request each.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    student2,problem1 = student2_problem1
    make_request(student2,problem1)
    assert(len(queue()) == 2)
    end()
    assert not queue()

def test_two_student_make_two_valid_one_invalid_request(student1_problem1,student2_problem1,student2_problem2):
    """
    two students each make one valid request each.
    one of the students will attempt to make another request.
    this request will raise a KeyError.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    student2,problem1 = student2_problem1
    make_request(student2,problem1)
    assert(len(queue()) == 2)
    # there is already a request from student2 in the queue.
    with pytest.raises(KeyError):
        student2,problem2 = student2_problem2
        make_request(student2,problem2)
    end()
    assert not queue()

def test_one_student_make_one_invalid_request(student1_badproblem1):
    """
    one student makes a request that will raise a ValueError.
    """
    end()
    # cannot make request where problem desc is empty string.
    with pytest.raises(ValueError):
        student1,badproblem1 = student1_badproblem1
        make_request(student1,badproblem1)
    end()
    assert not queue()

#################################################
# tests remaining() and help().                 #
#################################################

def test_remaining_no_requests(student1_problem1):
    """
    no requests made.
    remaining() will raise a KeyError.
    """
    end()
    student1,_ = student1_problem1
    with pytest.raises(KeyError):
        remaining(student1)
    end()
    assert not queue()

def test_help_no_requests(student1_problem1):
    """
    no requests made. 
    help() will raise a KeyError.
    """
    end()
    student1,_ = student1_problem1
    with pytest.raises(KeyError):
        help(student1)
    end()
    assert not queue()

def test_remaining_one_request(student1_problem1):
    """
    one request made and set to waiting.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    # assume that if we are the first to submit request, our position is 0 in queue.
    assert(remaining(student1) == 0)
    end()
    assert not queue()

def test_remaining_two_request_one_being_helped(student1_problem1,student2_problem1):
    """
    two requests made and both set to waiting.
    the first request made is set to receiving.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    student2,problem1 = student2_problem1
    make_request(student2,problem1)
    # help student1's request.
    help(student1)
    # student2 should be first in line.
    assert(remaining(student2) == 0)
    assert(len(queue()) == 2)
    end()
    assert not queue()

def test_remaining_two_request_one_being_helped_then_helped_again(student1_problem1,student2_problem1):
    """
    two requests made and both set to waiting.
    the first request made is set to receiving.
    attempt to set the first request to be receiving again.
    help() will raise KeyError
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    student2,problem1 = student2_problem1
    make_request(student2,problem1)
    # help student1's request.
    help(student1)
    # student1's request is not in waiting status.
    with pytest.raises(KeyError):
        help(student1)
    end()
    assert not queue()

#################################################
# tests resolve() and cancel().                 #
#################################################

def test_resolve_no_request(student1_problem1):
    """
    no requests made.
    """
    end()
    student1,_ = student1_problem1
    with pytest.raises(KeyError):
        resolve(student1)
    end()
    assert not queue()

def test_resolve_one_request_not_helped(student1_problem1):
    """
    one request made set to waiting.
    resolving request will raise KeyError.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    with pytest.raises(KeyError):
        resolve(student1)
    end()
    assert not queue()

def test_resolve_one_request_is_helped(student1_problem1):
    """
    one request made set to waiting.
    request then set to receiving.
    request is resolved.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    help(student1)
    resolve(student1)
    assert not queue()
    end()
    assert not queue()

def test_cancel_no_request(student1_problem1):
    """
    no requests made.
    """
    end()
    student1,_ = student1_problem1
    with pytest.raises(KeyError):
        cancel(student1)
    end()
    assert not queue()

def test_cancel_one_request_not_helped(student1_problem1):
    """
    one request made set to waiting.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    cancel(student1)
    assert not queue()
    end()
    assert not queue()

def test_cancel_one_request_is_helped(student1_problem1):
    """
    one request made set to waiting.
    request then set to receiving.
    cancelling request will raise KeyError
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    help(student1)
    with pytest.raises(KeyError):
        cancel(student1)
    end()
    assert not queue()

#################################################
# tests revert().                               #
#################################################

def test_revert_no_request(student1_problem1):
    """
    no requests made.
    """
    end()
    student1,_ = student1_problem1
    with pytest.raises(KeyError):
        revert(student1)
    end()
    assert not queue()

def test_revert_one_request_not_helped(student1_problem1):
    """
    one request made set to waiting.
    revert() will raise KeyError.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    with pytest.raises(KeyError):
        revert(student1)
    end()
    assert not queue()

def test_revert_one_request_is_helped(student1_problem1):
    """
    one request made set to waiting.
    request then set to receiving.
    revert request.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    help(student1)
    revert(student1)
    assert(len(queue()) == 1)
    end()
    assert not queue()

#################################################
# tests reprioritise().                         #
#################################################

def test_reprioritise_no_request():
    """
    no requests made.
    """
    end()
    assert not queue()
    reprioritise()
    assert not queue()
    end()
    assert not queue()

def test_reprioritise_one_request(student1_problem1):
    """
    student makes one request.
    request is not resolved.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    assert(len(queue()) == 1)
    reprioritise()
    assert(len(queue()) == 1)
    end()
    assert not queue()

def test_reprioritise_one_student_two_request_other_student_one_request(student1_problem1,student1_problem2,student2_problem1,student1_problem3,student2_problem3):
    """
    first student makes and resolves one request.
    first student makes and resolves another request.
    second student makes and resolves one request.

    when first and second students each make another request.
    second student has higher priority.
    """
    end()
    student1,problem1 = student1_problem1
    make_request(student1,problem1)
    help(student1)
    resolve(student1)

    student1,problem2 = student1_problem2
    make_request(student1,problem2)
    help(student1)
    resolve(student1)

    student2,problem1 = student2_problem1
    make_request(student2,problem1)
    help(student2)
    resolve(student2)

    student1,problem3 = student1_problem3
    make_request(student1,problem3)
    student2,problem3 = student2_problem3
    make_request(student2,problem3)
    reprioritise()

    # second student has higher priority.
    assert(queue()[0]['zid'] == student2)

    end()
    assert not queue()
