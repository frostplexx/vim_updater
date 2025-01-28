from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import threading

PORT = int(os.environ.get('PORT', 8080))
FTP_PORT = int(os.environ.get('FTP_PORT', 2121))

class VimrcHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            with open('update_vimrc.sh', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404)

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(os.getcwd(), perm='elradfmw')
    
    handler = FTPHandler
    handler.authorizer = authorizer
    
    server = FTPServer(('', FTP_PORT), handler)
    print(f"FTP server started at port {FTP_PORT}")
    server.serve_forever()

if __name__ == '__main__':
    # Start FTP server in a separate thread
    ftp_thread = threading.Thread(target=start_ftp_server)
    ftp_thread.daemon = True
    ftp_thread.start()
    
    # Start HTTP server
    with HTTPServer(("", PORT), VimrcHandler) as httpd:
        print(f"HTTP server serving at port {PORT}")
        httpd.serve_forever()
