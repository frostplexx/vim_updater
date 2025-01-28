from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from urllib.request import urlopen
from urllib.error import URLError
from config import VIMRC_URL

PORT = int(os.environ.get('PORT', 8080))

class VimrcHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('update_vimrc.sh', 'r') as file:
                script_content = file.read()
            
            # Replace the URL placeholder with the actual URL from config
            script_content = script_content.replace(
                'VIMRC_URL="PLACEHOLDER"',
                f'VIMRC_URL="{VIMRC_URL}"'
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(script_content.encode('utf-8'))
        elif self.path == '/vimrc':
            try:
                with urlopen(VIMRC_URL) as response:
                    vimrc_content = response.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(vimrc_content)
            except URLError as e:
                self.send_error(500, f"Failed to fetch vimrc: {str(e)}")
        else:
            self.send_error(404)

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, VimrcHandler)
    print(f'Starting HTTP server on port {PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
