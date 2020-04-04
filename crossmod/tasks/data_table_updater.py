from crossmod.db.updater import CrossmodDataTableUpdater
import crossmod

@crossmod.celery.task
def perform_update():
    db_updater = CrossmodDataTableUpdater()
    db_updater.update_database_values()
