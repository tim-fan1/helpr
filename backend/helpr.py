'''
The core functions of the helpr application.
'''

import json

# Put the global variables that hold the complete state of the application here.

# queue is a list of dictionaries in the form:
# {
#     'zid': zid,
#     'description': description,
#     'status': status,
#     'priority': priority,
# }
def load_queue_list():
    try:
        with open("queue_list.json","r") as FILE:
            queue_list = json.load(FILE)
            return queue_list
    # "queue_list.json" does not exist.
    except IOError:
        queue_list = []
        save_queue_list(queue_list)
        return queue_list

def save_queue_list(queue_list):
    with open("queue_list.json","w+") as FILE:
        json.dump(queue_list,FILE)
        pass

# dictionary of (int) priorities indexed by (string) zid.
# zid with lowest priority value has received the least help.
def load_priority_dictionary():
    try:
        with open("priority_dictionary.json","r") as FILE:
            priority_dictionary = json.load(FILE)
            return priority_dictionary
    # "priority_dictionary.json" does not exist.
    except IOError:
        priority_dictionary = {}
        save_priority_dictionary(priority_dictionary)
        return priority_dictionary

def save_priority_dictionary(priority_dictionary):
    with open("priority_dictionary.json","w+") as FILE:
        json.dump(priority_dictionary,FILE)
        pass

def make_request(zid, description):
    '''
    Used by students to make a request. The request is put in the queue with a
    "waiting" status.

    Params:
      zid (str): The ZID of the student making the request.

      description (str): A brief description of what the student needs help
      with.

    Raises:
      ValueError: if the description is the empty string.

      KeyError: if there is already a request from this particular student in
      the queue.
    '''
    queue_list = load_queue_list()
    priority_dictionary = load_priority_dictionary()
    # raising errors.
    if description == "":
        raise ValueError
    for request in queue_list:
        if request['zid'] == zid:
            raise KeyError
    # appending new request.
    if zid not in priority_dictionary:
        priority_dictionary[zid] = 0
    new_request = {
        'zid': zid,
        'description': description,
        'status': 'waiting',
        'priority': priority_dictionary[zid],
    }
    queue_list.append(new_request)
    save_queue_list(queue_list)
    save_priority_dictionary(priority_dictionary)
    pass

def queue():
    '''
    Used by tutors to view all the students in the queue in order.

    Returns:
      (list of dict) : A list of dictionaries where each dictionary has the keys
      { 'zid', 'description', 'status' }. These correspond to the student's ZID,
      the description of their problem, and the status of their request (either
      "waiting" or "receiving").
    '''
    queue_list = load_queue_list()
    # creating queue for tutor to view.
    result = []
    for request in queue_list:
        new_dict = {
            'zid': request['zid'],
            'description': request['description'],
            'status': request['status'],
        }
        result.append(new_dict)
    return result

def remaining(zid):
    '''
    Used by students to see how many requests there are ahead of theirs in the
    queue that also have a "waiting" status.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the student does not have a request in the queue with a
      "waiting" status.

    Returns:
      (int) : The position as a number >= 0
    '''
    queue_list = load_queue_list()
    # raising errors.
    is_waiting_in_queue = False
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'waiting':
            is_waiting_in_queue = True
            break
    if not is_waiting_in_queue:
        raise KeyError
    # finding position of student in queue (out of the students waiting).
    position = 0
    for request in queue_list:
        # ignore students that are not waiting.
        if request['status'] != 'waiting':
            continue
        # the request is in waiting status.
        if request['zid'] == zid:
            break
        position += 1
    return position

def help(zid):
    '''
    Used by tutors to indicate that a student is getting help with their
    request. It sets the status of the request to "receiving".

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the given student does not have a request with a "waiting"
      status.
    '''
    queue_list = load_queue_list()
    # raising errors.
    is_waiting_in_queue = False
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'waiting':
            is_waiting_in_queue = True
            break
    if not is_waiting_in_queue:
        raise KeyError
    # setting status of request to be receiving.
    for request in queue_list:
        if request['zid'] == zid:
            request['status'] = 'receiving'
            break
    save_queue_list(queue_list)
    pass

def resolve(zid):
    '''
    Used by tutors to remove a request from the queue when it has been resolved.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the given student does not have a request in the queue with a
      "receiving" status.
    '''
    queue_list = load_queue_list()
    priority_dictionary = load_priority_dictionary()
    # raising errors.
    is_receiving_in_queue = False
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'receiving':
            is_receiving_in_queue = True
            break
    if not is_receiving_in_queue:
        raise KeyError
    # resolving request.
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'receiving':
            queue_list.remove(request)
            # lower priority of zid.
            priority_dictionary[zid] += 1
            break
    save_queue_list(queue_list)
    save_priority_dictionary(priority_dictionary)
    pass 

def cancel(zid):
    '''
    Used by students to remove their request from the queue in the event they
    solved the problem themselves before a tutor was a available to help them.

    Unlike resolve(), any requests that are cancelled are NOT counted towards
    the total number of requests the student has made in the session.

    Params:
      zid (str): The ZID of the student who made the request.

    Raises:
      KeyError: If the student does not have a request in the queue with a
      "waiting" status.
    '''
    queue_list = load_queue_list()
    # raising errors.
    is_waiting_in_queue = False
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'waiting':
            is_waiting_in_queue = True
            break
    if not is_waiting_in_queue:
        raise KeyError
    # cancelling request.
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'waiting':
            queue_list.remove(request)
            break
    save_queue_list(queue_list)
    pass 

def revert(zid):
    '''
    Used by tutors in the event they cannot continuing helping the student. This
    function sets the status of student's request back to "waiting" so that
    another tutor can help them.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: If the student does not have a request in the queue with a
      "receiving" status.
    '''
    queue_list = load_queue_list()
    # raising errors.
    is_receiving_in_queue = False
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'receiving':
            is_receiving_in_queue = True
            break
    if not is_receiving_in_queue:
        raise KeyError
    # reverting request.
    for request in queue_list:
        if request['zid'] == zid and request['status'] == 'receiving':
            request['status'] = 'waiting'
            break
    save_queue_list(queue_list)
    pass 

def reprioritise():
    '''
    Used by tutors toward the end of the help session to prioritize the students
    who have received the least help so far.

    The queue is rearranged so that if one student has made fewer non-cancelled
    requests than another student, they are ahead of them in the queue. The
    ordering is otherwise preserved; i.e. if a student has made the same number
    of requests as another student, but was ahead of them in the queue, after
    reprioritise() is called, they should still be ahead of them in the queue.
    '''
    def return_priority(request):
        return request['priority']

    queue_list = load_queue_list()
    queue_list.sort(key=return_priority)
    save_queue_list(queue_list)
    pass

def end():
    '''
    Used by tutors at the end of the help session. All requests are removed from
    the queue and any records of previously resolved requests are wiped.
    '''
    queue_list = []
    priority_dictionary = {}
    save_queue_list(queue_list)
    save_priority_dictionary(priority_dictionary)
    pass
