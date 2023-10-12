from config.settings import env

CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://localhost:55100")
