### Serveur Python

Créez un fichier `server.py` pour configurer le serveur HTTP.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/execute_task':
            # Appeler le script de tâche
            subprocess.run(['sudo', '/usr/local/bin/task_script.sh'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Tâche exécutée')
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
print('Démarrage du serveur à http://0.0.0.0:8080')
server.serve_forever()
```