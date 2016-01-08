# coding:utf-8
# function of facepp control

import time
import config
import pdb
from packages.facepp import API, File
from pprint import pformat

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
api = API(API_KEY, API_SECRET)
MIN_CONFIDENCE = 30
MIN_SIMILARITY = 75

#function copied from facepp's hello.py
def print_result(hint, result):
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
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

def createFaceGroup(name, path, group_name = 'test'):
    pdb.set_trace()
    #detect face
    detect_result = api.detection.detect(img = File(path), mode = 'normal')
    print_result('Detection result for {}:'.format(name), detect_result)
    person_name_list = []
    count = 1
    for each_face in detect_result['face']:
    
        face_id = each_face['face_id']
        
        # recognize(identify) the face 
        recognize_result = api.recognition.identify(key_face_id = [face_id], group_name = group_name)
        print_result('Recognize result:', recognize_result)
        
        if recognize_result['face'][0]['candidate'][0]['confidence'] > MIN_CONFIDENCE:
            print 'found similar face(s)'
            # add the face to this person
            found_person_name = recognize_result['face'][0]['candidate'][0]['person_name']
            add_face_result = api.person.add_face(person_name = found_person_name, face_id = face_id)
            person_name_list.append(found_person_name)
            print add_face_result
            personTrain(found_person_name)
        else:
            print 'didn\'t find a similar face'
            #create a new Person for this face in the group
            new_person_name = name + '_new_' + str(count)
            try:
                api.person.create(person_name = new_person_name, 
                    group_name = group_name,
                    face_id = face_id)
            except:
                count = count + 3
                new_person_name = name + '_new_' + time.ctime()
                api.person.create(person_name = new_person_name, 
                    group_name = group_name,
                    face_id = face_id)
            person_name_list.append(new_person_name)
            count = count + 1
            personTrain(new_person_name)
            
    #train the group
    result = api.recognition.train(group_name = group_name, type = 'all')
    session_id = result['session_id']
    # wait before the train completes
    while True:
        result = api.info.get_session(session_id = session_id)
        if result['status'] == u'SUCC':
            print_result('Async train result:', result)
            break
        time.sleep(1)
    return person_name_list

def createFaceSet(name, path, faceset_name = 'faceset_test'):
    pdb.set_trace()
    #detect face
    detect_result = api.detection.detect(img = File(path), mode = 'normal')
    print_result('Detection result for {}:'.format(name), detect_result)
    similar_face_list = []
    for each_face in detect_result['face']:
        face_id = each_face['face_id']
        # recognize(search) the new face
        recognize_result = api.recognition.search(key_face_id = face_id, faceset_name = faceset_name)
        print_result('Recognize result:', recognize_result)
        face_list = [face['face_id'] for face in recognize_result['candidate'] if face['similarity'] > MIN_SIMILARITY]
        similar_face_list.extend(face_list)
        if similar_face_list:
            print 'found similar face(s)'
        # add the face to this faceset
        add_face_result = api.faceset.add_face(faceset_name = faceset_name, face_id = face_id)
        print add_face_result
        print similar_face_list
            
    #train the faceset
    result = api.train.search(faceset_name = faceset_name)
    session_id = result['session_id']
    # wait before the train completes
    while True:
        result = api.info.get_session(session_id = session_id)
        if result['status'] == u'SUCC':
            print_result('Async train result:', result)
            break
        time.sleep(1)
    return similar_face_list

def personTrain(person_name, type = 'all'):
    result = api.train.verify(person_name = person_name)
    session_id = result['session_id']
    # wait before the train completes
    while True:
        result = api.info.get_session(session_id = session_id)
        if result['status'] == u'SUCC':
            print_result('Async train result:', result)
            break
        time.sleep(1)
        
def groupTrain(group_name, type = 'all'):
    result = api.recognition.train(group_name = group_name, type = type)
    session_id = result['session_id']
    # wait before the train completes
    while True:
        result = api.info.get_session(session_id = session_id)
        if result['status'] == u'SUCC':
            print_result('Async train result:', result)
            break
        time.sleep(1)
        
def trainAllPerson():
    result = api.info.get_person_list()
    for each_person in result['person']:
        person_name = each_person['person_name']
        personTrain(person_name)
        
def main():
    path = 'static/images/test2.jpg'
    name = 'test2'
    createFaceSet(name = name, path = path)
    
if __name__ == '__main__':
    main()