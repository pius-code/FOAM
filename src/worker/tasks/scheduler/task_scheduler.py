from src.worker.tasks.reminder_task import print_reminder
from src.worker.celery_app import celery_app


@celery_app.task(name="src.worker.tasks.scheduler.task_scheduler.schedule_reminder")
def schedule_reminder() -> None:
    """Schedule a reminder task to run after a specified delay."""
    print("I am the scheduler")
    print_reminder("I am the task reminder")
