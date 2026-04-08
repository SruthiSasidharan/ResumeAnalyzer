"""
ASGI config for AI Career Guidance project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guidance.settings')
application = get_asgi_application()
