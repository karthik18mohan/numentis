import http.server,socketserver,os,sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self,path):
        p=path.split('?')[0].split('#')[0]
        if p!='/' and '.' not in os.path.basename(p): p+='.html'
        return super().translate_path(p)
    def do_POST(self):
        b=b'{"ok":true,"delivered":false}' if self.path.startswith('/api/lead') else b'{"ok":false}'
        self.send_response(200 if b'true' in b else 404);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b)
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
socketserver.TCPServer(('127.0.0.1',int(os.environ.get('NUMENTIS_PORT','8790'))),H).serve_forever()
