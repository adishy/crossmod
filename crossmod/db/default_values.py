from crossmod.db.interface import CrossmodDB
from crossmod.db.tables import ActiveSubredditsTable
from crossmod.db.tables import SubredditSettingsTable
from crossmod.helpers.consts import CrossmodConsts

def add_subreddit_to_monitor(db, 
                             subreddit_name, 
                             moderator_list, 
                             perform_action = False,
                             subreddit_classifiers = CrossmodConsts.SUBREDDIT_LIST, 
                             norm_classifiers = CrossmodConsts.NORM_LIST):
    db.write(SubredditSettingsTable,
            subreddit = subreddit_name,
            moderator_list = moderator_list.join(","),
            subreddit_classifiers = subreddit_classifiers,
            norm_classifers = norm_classifiers)

    db.write(ActiveSubredditsTable, 
             subreddit = subreddit_name,
             perform_action = perform_action)
    
    print(f"{subreddit_name} will be monitored")

def main():
    db = CrossmodDB()

    add_subreddit_to_monitor("modbot_staging", 
                             ["thebiglebowskiii"], 
                             True)

    add_subreddit_to_monitor("Futurology",
                             ["thebiglebowskiii", 
                             "AutoModerator", 
                             "TransPlanetInjection", 
                             "Xenophon1", 
                             "ion-tom", 
                             "mind_bomber",
                             "Gobi_The_Mansoe",
                             "multi-mod",
                             "Buck-Nasty",
                             "Yosarian2",
                             "ImLivingAmongYou",
                             "lughnasadh"])

if __name__=="__main__":
    main()
