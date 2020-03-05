from crossmod.db.interface import CrossmodDB
from crossmod.db.tables import SubredditSettingsTable
from crossmod.environments.consts import CrossmodConsts

def add_subreddit_to_monitor(db, 
                             subreddit_name, 
                             perform_action = False,
                             subreddit_classifiers = CrossmodConsts.SUBREDDIT_LIST, 
                             norm_classifiers = CrossmodConsts.NORM_LIST):
    db.write(SubredditSettingsTable,
            subreddit = subreddit_name,
            subreddit_classifiers = ",".join(subreddit_classifiers),
            norm_classifiers = ",".join(norm_classifiers),
            perform_action = perform_action)
    
    print(f"{subreddit_name} will be monitored")

def main():
    db = CrossmodDB()

    add_subreddit_to_monitor(db,
                             "modbot_staging", 
                             True)

    add_subreddit_to_monitor(db,
                             "Futurology")

if __name__=="__main__":
    main()
