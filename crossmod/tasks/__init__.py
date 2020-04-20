import crossmod
import crossmod.metrics
from crossmod.tasks.data_table_updater import perform_update
from crossmod.tasks.run_metrics import run_metrics
from celery.schedules import crontab

@crossmod.celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Update data table banned_at_utc, banned_by columns at 00:00 on Tuesday, Thursday and Saturday
    sender.add_periodic_task(crontab(minute="01", hour="00", day_of_week="2,4,6"), 
                             perform_update, name="perform_update")

    # Generate metrics for all subreddits
    sender.add_periodic_task(crontab(hour="*"), 
                             run_metrics, name="run_metrics")