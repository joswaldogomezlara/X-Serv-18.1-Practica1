#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import csv

class shortenerApp(webapp.webApp):

    URL_long_to_short = {}
    URL_short_to_long = {}

    try:
        with open('Short-Long.csv', 'r') as csvfile:
            URL_reader = csv.reader(csvfile)
            for row in URL_reader:
                URL_short_to_long[row[0]] = row[1]
    except IOError:
        with open('Short-Long.csv', 'w') as csvfile:
            URL_writer = csv.writer(csvfile)

    try:
        with open('Long-Short.csv', 'r') as csvfile:
            URL_reader = csv.reader(csvfile)
            for row in URL_reader:
                URL_long_to_short[row[0]] = row[1]
    except IOError:
        with open('Long-Short.csv', 'w') as csvfile:
            URL_writer = csv.writer(csvfile)

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        header = request.split(" ")[0]
        resource = request.split(" ")[1]

        try:
            body = request.split('\r\n\r\n')[-1]
        except:
            body = ''

        return [header, resource, body]

    def process(self, parsedRequest):
        """
        Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """        

        if parsedRequest[0] == 'GET' and parsedRequest[1] == '/':
            returnCode = '200 OK'
            htmlAnswer = ('<html><body><p>' +
                          'Estas son las URLs que el servidor maneja en este momento:' +
                          '</p></body></html>' +
                          '<p>' +
                          str(self.URL_long_to_short) +
                          '</p>' +
                          '<p>' +
                          'Introduce la URL que quieres acortar:' +
                          '</p>' +
                          '<FORM method="POST" action="http://localhost:1234">' +
                          '<INPUT type="text" name="URL para acortar">' +
                          '</FORM>')
        elif parsedRequest[0] == 'POST' and parsedRequest[1] == '/':
            URL_long = parsedRequest[2].split("=")[1]

            URL_long = URL_long.replace('%3A',':')
            URL_long = URL_long.replace('%2F','/')

            if URL_long.find('http://') == -1 and URL_long.find('https://') == -1:
                URL_long = 'http://' + URL_long
               

            if URL_long == 'http://':
                returnCode = '400 BAD REQUEST'
                htmlAnswer = ('<html><body><p>' +
                             'Has mandado una URL vacia' +
                             '</p>' +
                             '<p>Para volver a la pagina principal pinchar aqui: ' +
                             '<a href=http://localhost:1234>Main page</a>' +
                             '</p></body></html>')

            elif URL_long in self.URL_long_to_short:

                returnCode = '200 OK'
                htmlAnswer =    ('<html><body><p>URL acortada ya disponible: ' +
                                '<a href=' + URL_long + '>' + URL_long + '</a>' +
                                ' >>> ' +
                                '<a href=' + self.URL_long_to_short[URL_long] + '>' + 
                                self.URL_long_to_short[URL_long] + '</a>' +
                                '</p>' + 
                                '<p>Para volver a la pagina principal pinchar aqui: ' +
                                '<a href=http://localhost:1234>Main page</a>' +
                                '</p></body></html>')

            elif URL_long in self.URL_short_to_long:
                URL_short = URL_long

                returnCode = '200 OK'
                htmlAnswer =    ('<html><body><p>URL acortada ya disponible: ' +
                                '<a href=' + self.URL_short_to_long[URL_short] + '>' + 
                                self.URL_short_to_long[URL_short] + '</a>' +
                                ' >>> ' +
                                '<a href=' + URL_short + '>' + URL_short + '</a>' +
                                '</p>' + 
                                '<p>Para volver a la pagina principal pinchar aqui: ' +
                                '<a href=http://localhost:1234>Main page</a>' +
                                '</p></body></html>')

            else:
                URL_short = self.URL_upload(URL_long)
                returnCode = '200 OK'
                htmlAnswer =    ('<html><body><p>URL acortada: ' +
                                '<a href=' + URL_long + '>' + URL_long + '</a>' +
                                ' >>> ' +
                                '<a href=' + URL_short + '>' + URL_short + '</a>' +
                                '</p>' + 
                                '<p>Para volver a la pagina principal pinchar aqui: ' +
                                '<a href=http://localhost:1234>Main page</a>' +
                                '</p></body></html>')

        elif parsedRequest[0] == 'GET' and parsedRequest[1] != '/':
            request_resource = 'http://localhost:1234' + parsedRequest[1]

            if request_resource in self.URL_short_to_long:
                returnCode =    ('301 MOVED PERMANENTLY\r\n' +
                                'Location: ' + self.URL_short_to_long[request_resource])
                htmlAnswer = ''
            else:
                returnCode = '404 NOT FOUND'
                htmlAnswer = ('<html><body><p>' +
                             'Has solicitado un recurso que no existe' +
                             '</p>' +
                             '<p>Para volver a la pagina principal pinchar aqui: ' +
                             '<a href=http://localhost:1234>Main page</a>' +
                             '</p></body></html>')                    

        else:
            returnCode = '200 OK'
            htmlAnswer = "<html><body><h1>Peticion no prevista</h1></body></html>"

        return (returnCode, htmlAnswer)

    def URL_upload(self, URL_long):

        URL_short = 'http://localhost:1234/' + str(len(self.URL_long_to_short))
        self.URL_long_to_short[URL_long] = URL_short
        self.URL_short_to_long[URL_short] = URL_long

        with open('Long-Short.csv', 'w') as csvfile:
            URL_writer = csv.writer(csvfile)
            for row in self.URL_long_to_short:
                URL_writer.writerow([row] + [self.URL_long_to_short[row]])

        with open('Short-Long.csv', 'w') as csvfile:
            URL_writer = csv.writer(csvfile)
            for row in self.URL_short_to_long:
                URL_writer.writerow([row] + [self.URL_short_to_long[row]])

        return URL_short

if __name__ == "__main__":
    testWebApp = shortenerApp("localhost", 1234)









































