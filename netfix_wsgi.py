import os
import sys

# Add the netfix directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'netfix')))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netfix.settings')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Needed for gunicorn
app = application