from src.worker.celery_app import celery_app


@celery_app.task(name="src.worker.tasks.reminder_task")
def print_reminder(message: str) -> None:
    print(f"Reminder: {message}")
    return None
