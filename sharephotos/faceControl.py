# coding:utf-8
# function of facepp control

import time
import ConfigParser
import os
import sae.const
from packages.facepp import API, File
from pprint import pformat

cp = ConfigParser.ConfigParser()
cp.read('project.conf')
API_KEY = cp.get('FACEPP_API', 'API_KEY')
API_SECRET = cp.get('FACEPP_API', 'API_SECRET')
api = API(API_KEY, API_SECRET)
MIN_CONFIDENCE = 30
MIN_SIMILARITY = 60
DEFAULT_GROUP = 'spgroup'


def add_faces(method, url_or_path):
    """ Detect faces in the photo and add them to the faceset.  """

    result = group_train(group_name=DEFAULT_GROUP)
    if method == 'path':
        detect_result = api.recognition.identify(
            group_name=DEFAULT_GROUP, img=File(url_or_path), mode='normal')
    elif method == 'url':
        detect_result = api.recognition.identify(
            group_name=DEFAULT_GROUP, url=url_or_path, mode='normal')
    print_result('detect_result:', detect_result)

    # Ignore the situation that two faces of one person in the photo for now.
    # """
    person_list = []
    for each_face in detect_result['face']:
        face_id = each_face['face_id']
        person_id = find_person(each_face)
        if not person_id:
            # Create a new person into the group
            person_id = api.person.create(face_id=face_id)['person_id']
            result = api.group.add_person(
                group_name=DEFAULT_GROUP, person_id=person_id)
            print 'create new person'
        # Add the face to the person
        result = api.person.add_face(person_id=person_id, face_id=face_id)
        if result['success']:
            print 'add face to person Ok'
        else:
            print 'add face to person failed'
        person_list.append(person_id)

    return person_list


def find_person(each_face):
    if each_face['candidate'] and\
            each_face['candidate'][0]['confidence'] > MIN_CONFIDENCE:
        return each_face['candidate'][0]['person_id']
    else:
        return False


def person_train(person_name, type='all'):
    """ Train the faces of a person. """

    result = api.train.verify(person_name=person_name)
    session_id = result['session_id']
    return get_result(session_id)


def group_train(group_name, type='all'):
    """ Train the group. """

    result = api.recognition.train(group_name=group_name, type=type)
    session_id = result['session_id']
    return get_result(session_id)


def get_result(session_id):
    """ Wait before the train completes. """

    start_time = time.time()
    while time.time() - start_time < 20:
        result = api.info.get_session(session_id=session_id)
        if result['status'] == u'SUCC':
            print_result('Async train result:', result)
            return True
        time.sleep(1)
    return False


def train_all_person():
    """ Train faces of all persons. """

    result = api.info.get_person_list()
    for each_person in result['person']:
        person_name = each_person['person_name']
        personTrain(person_name)


def print_result(hint, result):
    """ Function copied from facepp's hello.py.  """

    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width=75).split('\n')])
