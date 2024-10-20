from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = int(os.environ.get('PORT', 8080))

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

if __name__ == '__main__':
    with HTTPServer(("", PORT), VimrcHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
