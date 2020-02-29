import os

class CrossmodConsts:
    PERSPECTIVE_API_SECRET = os.environ['PERSPECTIVE_API_SECRET']
    REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
    REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']
    ENVIRONMENT="debug"
    DB_PATH = os.environ['DB_PATH']
    MODELS_DIRECTORY = os.environ['MODELS_DIRECTORY']
    SUBREDDIT_CLASSIFIERS = "subreddit"
    NORM_CLASSIFIERS = "norm"
    SUBREDDIT_LIST = ['The_Donald', 'politics', 'AskReddit', 'science', 'worldnews', 'news', 'explainlikeimfive', 'relationships', 'TwoXChromosomes', 'gonewild', 'hillaryclinton', 'askscience', 'leagueoflegends', 'AskHistorians', 'Games', 'PoliticalDiscussion', 'personalfinance', 'aww', 'photoshopbattles', 'syriancivilwar', 'nosleep', 'CFB', 'pcmasterrace', 'pics', 'pokemongo', 'funny', 'GlobalOffensive', 'Futurology', 'SandersForPresident', 'MMA', 'europe', 'nfl', 'EnoughTrumpSpam', 'BlackPeopleTwitter', 'pokemontrades', 'legaladvice', 'history', 'videos', 'AskWomen', 'sex', 'GlobalOffensiveTrade', 'LateStageCapitalism', 'gaming', 'whatisthisthing', 'Showerthoughts', 'DIY', 'Android', 'OutOfTheLoop', 'atheism', 'UpliftingNews', 'Incels', 'gifs', 'food', 'movies', 'india', 'books', 'depression', 'hiphopheads', 'pokemon', 'philosophy', 'nba', 'Christianity', 'anime', '2007scape', 'fantasyfootball', 'Overwatch', 'tifu', 'churning', 'changemyview', 'space', 'conspiracy', 'ShitRedditSays', 'canada', 'socialism', 'soccerstreams', 'CanadaPolitics', 'nottheonion', 'gameofthrones', 'OldSchoolCool', 'AskTrumpSupporters', 'creepyPMs', 'SuicideWatch', 'wow', 'LifeProTips', 'SubredditDrama', 'technology', 'TheSilphRoad', 'hearthstone', 'spacex', 'me_irl', 'IAmA', 'DestinyTheGame', 'television', 'dataisbeautiful', 'NSFW_GIF', 'PurplePillDebate', 'GetMotivated', 'asoiaf', 'NeutralPolitics', 'jailbreak' ]
    NORM_LIST = ['misogynistic-slurs', 'verbal-attacks-on-Reddit', 'hatespeech-racist-homophobic', 'porno-links', 'abusing-and-criticisizing-mods', 'namecalling-claiming-other-too-sensitive', 'personal-attacks', 'opposing-political-views-trump']
    AGREEMENT_SCORE_THRESHOLD = 0.85
    CLIENT_API_ENDPOINT = "http://localhost/api/v1/get-prediction-scores"
    CLIENT_API_SUPER_KEY = "ABCDEFG"

    @staticmethod
    def get_norms_classifier(norm):
        NORMS_CLASSIFIERS = CrossmodConsts.MODELS_DIRECTORY + "/norm-clfs/"
        return NORMS_CLASSIFIERS + "model_" + norm + ".bin"

    @staticmethod
    def get_subreddit_classifier(subreddit):
        SUBREDDIT_CLASSIFIERS = CrossmodConsts.MODELS_DIRECTORY + "/subreddit-clfs/"
        return SUBREDDIT_CLASSIFIERS + "model_" + subreddit + ".bin"

def main():
    print("Perpective API Key: ",      CrossmodConsts.PERSPECTIVE_API_SECRET)
    print("Reddit Client UserAgent:",  CrossmodConsts.REDDIT_USER_AGENT)
    print("Reddit Client ID: ",        CrossmodConsts.REDDIT_CLIENT_ID)
    print("Reddit Client Secret",      CrossmodConsts.REDDIT_CLIENT_SECRET)
    print("Reddit Password: ",         CrossmodConsts.REDDIT_PASSWORD)
    print("Reddit Username: ",         CrossmodConsts.REDDIT_USERNAME)
    print("Database path: ",           CrossmodConsts.DB_PATH)
    print("Norms model: ",             CrossmodConsts.get_norms_classifier('verbal-attacks-on-Reddit'))
    print("Subreddit model: ",         CrossmodConsts.get_subreddit_classifier('Futurology'))

if __name__ == "__main__":
    main()
