#  coding: utf-8 
import SocketServer, os, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Shuming Zhang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        # Check if the request method is GET
        if self.data.split()[0] == "GET":
            # Redirect http://127.0.0.1:8080/deep to http://127.0.0.1:8080/deep/
            # https://en.wikipedia.org/wiki/HTTP_302
            if self.data.split()[1] == "/deep":
                self.request.sendall("HTTP/1.1 302 Found\r\n" +
                                     "Location: http://127.0.0.1:8080/deep/\r\n" +
                                     "\r\n")
            else:
                # https://docs.python.org/2/library/os.path.html
                filepath = os.path.abspath(os.getcwd() + "/www" + self.data.split()[1])

                # Check if the path is under www/
                if (os.getcwd() + "/www") in filepath:
                    # Redirect the directory to index.html
                    if os.path.isdir(filepath):
                        filepath += "/index.html"

                    # Check if the file exists
                    if os.path.isfile(filepath):
                        # https://docs.python.org/2/library/mimetypes.html
                        filetype = mimetypes.guess_type(filepath)[0]
                        self.request.sendall("HTTP/1.1 200 OK\r\n" +
                                             "Content-Type: " + filetype + "\r\n" +
                                             "\r\n" +
                                             open(filepath).read())
                    else:
                        self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n")
                else:
                    self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n")

        else:
            self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n")



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()




