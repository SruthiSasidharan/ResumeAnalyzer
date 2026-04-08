"""
WSGI config for AI Career Guidance project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guidance.settings')
application = get_wsgi_application()
