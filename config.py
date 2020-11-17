import os

TEMPLATE_DIR = os.environ.get('TEMPLATES') or 'templates'
TZ_NAME = os.environ.get('TZ_NAME') or 'US East'
TZ_OFFSET = os.environ.get('TZ_OFFSET') or -5
SCHEDULE_PATH = os.environ.get('SCHEDULE_PATH') or 'stuyfall20.csv'
SCHEDULE_TIMES = os.environ.get('SCHEDULE_TIMES') or 'stuyfall20times.csv'
USERS_DB = os.environ.get('USERS_DB') or 'users.db'
NUM_PERIODS = os.environ.get('NUM_PERIODS') or 10
HW_DB = os.environ.get('HW_DB') or 'hw.db'
