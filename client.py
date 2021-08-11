import http.client
import json
import threading
import time


def send_msg(name_header, connection):
    while True:
        msg = input()
        headers = {'Content-type': 'application/json', 'user': name_header}
        data = json.dumps({'msg': msg})
        connection.request('POST', '/', data, headers)
        response = connection.getresponse()


def get_msg(name_header, connection):
    while True:
        headers = {'Content-type': 'application/json', 'user': name_header}
        connection.request('GET', '/', headers= headers)
        response = connection.getresponse()
        response_data = json.loads(response.read().decode())
        if response_data['status'] == 'new message':
            print(response_data['user'], ' : ', response_data['message'])


if __name__ == '__main__':
    conn = http.client.HTTPConnection('127.0.0.1', 8080)
    name = input('name : ')
    headers = {'Content-type': 'application/json'}
    name_json = {'name': name}
    json_data = json.dumps(name_json)
    conn.request('POST', '/join', json_data, headers)
    response = conn.getresponse()
    conn.close()
    name_header = json.loads(response.read().decode())['name_header']
    print('welcome to the chat room ...')
    t1 = threading.Thread(target=send_msg, args=(name_header, http.client.HTTPConnection('127.0.0.1', 8080), ))
    t2 = threading.Thread(target=get_msg, args=(name_header, http.client.HTTPConnection('127.0.0.1', 8080), ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()