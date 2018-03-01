"""
Ex:
import imgurauth
imgurAuth = imgurauth.TokenHandler(os.environ['IMGUR_APP_ID'])
access_token = imgurAuth.get_access_token()

import imgurauth
imgurAuth = imgurauth.TokenHandler("3bb4ea8e2954a26")
tokens = imgurAuth.get_access_token()

"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urllib2 import urlopen, HTTPError
from webbrowser import open_new

REDIRECT_URL = 'http://localhost:8080/'
PORT = 8080


class HTTPServerHandler(BaseHTTPRequestHandler, object):

    """
    HTTP Server callbacks to handle imgur OAuth redirects
    """
    def __init__(self, request, address, server, c_id):
        self.client_id = c_id
        super(HTTPServerHandler, self).__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #print(self.path)
        if not '?' in self.path:
            # send javascript
            self.wfile.write(bytes("""<html><script type=text/javascript>// First, parse the query string
var params = {}, queryString = location.hash.substring(1),
    regex = /([^&=]+)=([^&]*)/g, m;
while (m = regex.exec(queryString)) {
  params[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
}

// And send the token over to the server
var req = new XMLHttpRequest();
// consider using POST so query isn't logged
req.open('GET', 'http://localhost:8080/catchtoken?' + queryString, true);

req.onreadystatechange = function (e) {
  if (req.readyState == 4) {
     if(req.status == 200){
       //window.location = params['state']
       alert('You may now close this window.')
   }
  else if(req.status == 400) {
        alert('There was an error processing the token.')
    }
    else {
      alert('something else other than 200 was returned')
    }
  }
};
req.send(null);</script></html>"""))

        # we got our tokens here
        if '/catchtoken?' in self.path:
            
            a_token = self.path.split("access_token=")[1]
            a_token = a_token.split('&')[0]
            r_token = self.path.split("refresh_token=")[1]
            r_token = r_token.split('&')[0]
            
            self.server.access_token = a_token
            self.server.refresh_token = r_token

    # Disable logging from the HTTP Server
    def log_message(self, format, *args):
        return


class TokenHandler:
    """
    Functions used to handle imgur oAuth
    """
    def __init__(self, c_id):
        self._id = c_id

    def get_access_token(self):
        """
         Fetches the access key using an HTTP server to handle oAuth
         requests
            Args:
                clientId: the imgur assigned client id
        """

        ACCESS_URI = ("https://api.imgur.com/oauth2/authorize?client_id="+self._id+"&response_type=token")

        open_new(ACCESS_URI)
        httpServer = HTTPServer(
                ('localhost', PORT),
                lambda request, address, server: HTTPServerHandler(
                    request, address, server, self._id))
        # send javascript
        httpServer.handle_request()
        # get tokens
        httpServer.handle_request()
        return (httpServer.access_token,httpServer.refresh_token) 
