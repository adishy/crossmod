from crossmod.db import CrossmodDB, SubredditSettingsTable
import crossmod
import crossmod.metrics as metrics


@crossmod.celery.task
def run_metrics():
    db = CrossmodDB()

    print("Generating Metrics:")
 
    for row in db.database_session.query(SubredditSettingsTable.subreddit).all():
        subreddit = row.subreddit
        print("____________________________________________")
        print("Subreddit:", subreddit)

        print("Rate of Crossmod Reports: starting")
        metrics.RateOfCrossmodReports(subreddit).save_plot()
        print("Rate of Crossmod Reports: done ✔️")

        print("Rate of Moderator Removals: starting")
        metrics.RateOfModeratorRemovals(subreddit).save_plot()
        print("Rate of Moderator Removals: done ✔️")

        print("Rate of Report Removal Sequences: starting")
        metrics.RateOfReportRemovalSequences(subreddit).save_plot()
        print("Rate of Report Removal Sequences: done ✔️")

        print("Rate of Reports With Removals: starting")
        metrics.RateOfReportsWithRemovals(subreddit).save_plot()
        print("Rate of Report With Removals: done ✔️")

        print("Rate of Total Comments: starting")
        metrics.RateOfTotalComments(subreddit).save_plot()
        print("Rate of Total Comments: done ✔️")

        print("Agreement Score vs Comments: starting")
        metrics.AgreementScoreVsComments(subreddit).save_plot()
        print("Agreement Score vs Comments: done ✔️")
        print("____________________________________________")
