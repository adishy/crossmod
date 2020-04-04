import crossmod
from crossmod.tasks.data_table_updater import perform_update
from celery.schedules import crontab

@crossmod.celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Update data table banned_at_utc, banned_by columns at 00:00 on Tuesday, Thursday and Saturday
    sender.add_periodic_task(crontab(minute="01", hour="00", day_of_week="2,4,6"), 
                             perform_update, name="perform_update")