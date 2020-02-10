import crossmod
from crossmod.db.interface import CrossmodDB
from crossmod.db.tables import DataTable
from crossmod.helpers.consts import CrossmodConsts
from sqlalchemy import func

def current_overall_stats(crossmod_agreement_score = CrossmodConsts.AGREEMENT_SCORE_THRESHOLD):
    db = CrossmodDB()
    crossmod_state = {}

    crossmod_state['total_comments'] = db.database_session.query(func.count(DataTable.id)).scalar()
    crossmod_state['automoderator'] = db.database_session.query(func.count(DataTable.banned_by == 'AutoModerator')).scalar()
    crossmod_state['moderators'] = db.database_session.query(DataTable).filter(DataTable.banned_by != 'AutoModerator', DataTable.banned_by != None).count()
    crossmod_state['crossmod_agreement_score'] = db.database_session.query(DataTable).filter(DataTable.agreement_score >= crossmod_agreement_score).count()
    crossmod_state['automoderator_and_crossmod'] = db.database_session.query(DataTable).filter(DataTable.agreement_score > crossmod_agreement_score, DataTable.banned_by == 'AutoModerator').count()
    crossmod_state['moderators_and_crossmod'] = db.database_session.query(DataTable).filter(DataTable.agreement_score > crossmod_agreement_score, DataTable.banned_by != 'AutoModerator', DataTable.banned_by != None).count()
    crossmod_state['only_crossmod'] = db.database_session.query(DataTable).filter(DataTable.agreement_score > crossmod_agreement_score, DataTable.banned_by == None).count()

    return crossmod_state