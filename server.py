from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from socketserver import ThreadingMixIn

hostName = "localhost"
serverPort = 8080


class Server(BaseHTTPRequestHandler):
    users = {}
    users_msgs = []
    def do_GET(self):
        user = self.users[self.headers['user']]
        msg_count = len(self.users_msgs)
        for i in range(1, 5000):
            if msg_count < len(self.users_msgs) and self.users_msgs[msg_count][0] == user:
                msg_count += 1
            elif msg_count < len(self.users_msgs) and self.users_msgs[msg_count][0] != user:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                data = {'status': 'new message', 'user': self.users_msgs[msg_count][0], 'message': self.users_msgs[msg_count][1]}
                self.wfile.write(bytes(json.dumps(data), 'utf-8'))
                return None
            time.sleep(0.001)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = {'status': 'no message'}
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))


    def do_POST(self):
        if self.path == '/join':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            name = json.loads(self.rfile.read(content_length))['name']
            hash_name = str(hash(str(time.time())))
            self.users[hash_name] = name
            self.wfile.write(bytes(json.dumps({'name_header': hash_name}), 'utf-8'))
            print(self.users)
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            user = self.users[self.headers['user']]
            msg = json.loads(data)['msg']
            self.users_msgs.append((user, msg))
            self.wfile.write(bytes(json.dumps({'status': 'ok', 'path': self.path}), 'utf-8'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == "__main__":
    webServer = ThreadedHTTPServer((hostName, serverPort), Server)
    print("Server started ...")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")