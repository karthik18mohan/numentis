import http.server,socketserver,os,sys
os.chdir('/home/claude/numentis-v2')
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self,path):
        p=path.split('?')[0].split('#')[0]
        if p!='/' and '.' not in os.path.basename(p): p+='.html'
        return super().translate_path(p)
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
socketserver.TCPServer(('127.0.0.1',8765),H).serve_forever()
