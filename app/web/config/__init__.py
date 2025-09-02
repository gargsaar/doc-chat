import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    
    # Worker/Redis execution control
    USE_WORKERS = os.environ.get("USE_WORKERS", "false").lower() in ("true", "1", "yes", "on")
    REDIS_URI = os.environ.get("REDIS_URI")
    
    # Only enable Celery workers if both USE_WORKERS=true and REDIS_URI is provided
    CELERY_ENABLED = USE_WORKERS and bool(REDIS_URI)
    
    CELERY = {
        "broker_url": REDIS_URI if CELERY_ENABLED else "memory://",
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
        "task_always_eager": not CELERY_ENABLED,  # Run synchronously if workers disabled
        "task_eager_propagates": True,  # Propagate exceptions in sync mode
    }
