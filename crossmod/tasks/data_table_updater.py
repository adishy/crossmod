from crossmod.db.updater import CrossmodDataTableUpdater
import crossmod

@crossmod.celery.task
def perform_db_update():
    db_updater = CrossmodDataTableUpdater()
    db_updater.update_database_values()

@crossmod.celery.task
def test(args):
    print("Task", args)