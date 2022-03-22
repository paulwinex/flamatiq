import os


REDIS_HOST = os.getenv('REDIS_HOST') or (os.getenv('APP_NAME')+'-redis' if os.getenv('APP_NAME') else None) or 'localhost'

