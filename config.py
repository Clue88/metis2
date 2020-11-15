import os

TEMPLATE_DIR = os.environ.get('TEMPLATES') or 'templates'
TZ_NAME = os.environ.get('TZ_NAME') or 'US East'
TZ_OFFSET = os.environ.get('TZ_OFFSET') or -5
