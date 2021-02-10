from crossmod.db.interface import CrossmodDB
from crossmod.db.tables import SubredditSettingsTable
from crossmod.environments.consts import CrossmodConsts


def add_subreddit_to_monitor(db, 
                             subreddit_name, 
                             perform_action = False,
                             subreddit_classifiers = CrossmodConsts.subreddit_list(), 
                             norm_classifiers = CrossmodConsts.norm_list()):
    db.write(SubredditSettingsTable,
            subreddit = subreddit_name,
            subreddit_classifiers = ",".join(subreddit_classifiers),
            norm_classifiers = ",".join(norm_classifiers),
            perform_action = perform_action)
    
    print(f"{subreddit_name} will be monitored")


def main():
    db = CrossmodDB()

    subreddits = [("modbot_staging", True),
                  ("Futurology", False),
                  ("Coronavirus", False),
                  ("China_Flu", False)]

    for subreddit in subreddits:
        add_subreddit_to_monitor(db, subreddit[0], subreddit[1])


if __name__=="__main__":
    main()
