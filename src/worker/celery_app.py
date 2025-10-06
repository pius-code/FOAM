from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "foam",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.worker.tasks.scheduler.task_scheduler"],
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    Timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
)


celery_app.conf.beat_schedule = {
    "foam_worker": {
        "task": "src.worker.tasks.scheduler.task_scheduler.schedule_reminder",
        "schedule": 60.0,
    }
}
