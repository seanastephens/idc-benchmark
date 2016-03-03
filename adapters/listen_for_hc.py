import BaseHTTPServer
import sys

# IMPORTANT: This doesn't work right now!
#
# Wait on specified port for a single GET, then quit. The hashedcube server
# sends us a request when it is ready, and this program simply waits for that
# request. Useful for blocking scripts until the server is ready, but for now I
# am doing that with `sleep n` in bash (don't want to touch libcurl again for a
# little while).

class GETHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200)

class OneRequestServer(BaseHTTPServer.HTTPServer):
    def serve_forever(self):
        self.handle_request()

if __name__ == "__main__":
    OneRequestServer(("localhost", 4001), GETHandler).serve_forever()
    sys.exit(17)
