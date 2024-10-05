from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from utils.generate_report import generate_report_task

scheduler = None


def start():
    global scheduler
    if scheduler is None or not scheduler.running:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            generate_report_task,
            'interval',
            minutes=0.3,
            name='check_database_job',
            replace_existing=True,
        )

        scheduler.start()