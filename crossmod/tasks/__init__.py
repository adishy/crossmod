import crossmod
from crossmod.tasks.db_updater import perform_db_update, test

@crossmod.celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1.0, test.s("a"), name="test")