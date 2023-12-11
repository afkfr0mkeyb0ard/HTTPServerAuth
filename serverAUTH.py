from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from ntlm_auth.ntlm import Ntlm
from base64 import b64decode

class NTLMHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'NTLM')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write(b'Unauthorized1')
        else:
            try:
                auth = Ntlm()
                print('Credentials:', self.headers.get('Authorization'))
                auth.authenticate(self.headers.get('Authorization'))
                SimpleHTTPRequestHandler.do_GET(self)
            except:
                self.do_AUTHHEAD()
                self.wfile.write(b'Unauthorized2')

class BasicAuthHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Hi\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write(b'Unauthorized1')
        else:
            auth = self.headers.get('Authorization')
            _, encoded = auth.split(' ', 1)
            decoded = b64decode(encoded).decode('utf-8')
            print(decoded)
            username, password = decoded.split(':', 1)
            if username == 'zefzefzefzefze' and password == 'zefzefzefezef':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Test page')
            else:
                self.do_AUTHHEAD()
                self.wfile.write(b'Unauthorized2')

server_address = ('0.0.0.0', 8000)
#httpd = HTTPServer(server_address, NTLMHandler)
httpd = HTTPServer(server_address, BasicAuthHandler)
httpd.serve_forever()