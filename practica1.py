#!/usr/bin/python

import socket
import csv

class webApp:

    def URLs_update(self, URL_long)


    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        header = request.split(" ")[0]
        resource = request.split(" ")[1]
        body = request.split(" ")[-1]

        return [header, resource, body]

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        if parsedRequest[0] == 'GET' and parsedRequest[1] == '/':
            returnCode = '200 OK'
            htmlAnswer = ('<html><body><p>Introduzca la URL que desea acortar' +
                          '</p></body></html>' +
                          '<FORM method="POST" action="http://localhost:1234">' +
                          '<INPUT type="text" name="URL_para_acortar">' +
                          '</FORM>')
        elif parsedRequest[0] == 'POST' and parsedRequest[1] == '/':
            URL_long = parsedRequest[2].split("=")[1]

            if URL_long = '':
                returnCode = '400 BAD REQUEST'
                htmlAnswer = "<html><body><p>No has mandado una URL valida</p></body></html>"
            else:
                returnCode = '200 OK'
                htmlAnswer = "<html><body><p>URL recibida</p></body></html>"

            URL_short = self.URLs_update(URL_long)

        else:
            returnCode = '200 OK'
            htmlAnswer = "<html><body><h1>Peticion no prevista</h1></body></html>"

        return (returnCode, htmlAnswer)

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print 'Answering back...'
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)









































