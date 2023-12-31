"""
WSGI config for harvester project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harvester.settings")

from .utils import harvester_init
from .utils import comunication_harvester_synthesis

project_list = harvester_init()

application = get_wsgi_application()

comunication_harvester_synthesis(project_list=project_list)

