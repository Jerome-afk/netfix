import os
import sys
import subprocess

# This script serves as an entry point for starting the Django application
# It will be called by gunicorn in the workflow configuration

def app(environ, start_response):
    """
    Simple WSGI application that redirects all requests to the Django server
    """
    start_response('302 Found', [('Location', 'http://0.0.0.0:8000/')])
    return [b'Redirecting to Django application...']

if __name__ == "__main__":
    # Start the Django server
    os.chdir('netfix')
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])