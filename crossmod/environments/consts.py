import os

class CrossmodConsts:
    if os.environ.get("DOWNLOAD_MODELS"):
        print("Downloading models!")
        from crossmod.b2_model_store import b2_download_models
        b2_download_models()

    # Reddit account used to run Crossmod
    REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']

    # Reddit UA value (let Reddit know this is a bot)
    REDDIT_USER_AGENT = "Crossmod (by /u/CrossModerator, for more details visit crossmod.ml)"

    # Subreddit Monitor Client ID and Secret
    MONITOR_REDDIT_CLIENT_ID = os.environ['MONITOR_REDDIT_CLIENT_ID']
    MONITOR_REDDIT_CLIENT_SECRET = os.environ['MONITOR_REDDIT_CLIENT_SECRET']
    
    # DB Updater Client ID and Secret
    UPDATER_REDDIT_CLIENT_ID = os.environ['UPDATER_REDDIT_CLIENT_ID']
    UPDATER_REDDIT_CLIENT_SECRET = os.environ['UPDATER_REDDIT_CLIENT_SECRET']
    
    ENVIRONMENT="debug"

    # Database file path
    DB_PATH = os.environ['DB_PATH']

    # Directory with fasttext models
    MODELS_DIRECTORY = os.environ['MODELS_DIRECTORY']

    # Full list of subreddit classifiers
    #SUBREDDIT_LIST = CrossmodConsts.subreddit_list()()
    
    # Full list of norm classifiers
    #NORM_LIST = CrossmodConsts.norm_list()()

    SUBREDDIT_CLASSIFIERS = "subreddit"
    NORM_CLASSIFIERS = "norm"

    AGREEMENT_SCORE_THRESHOLD = 0.85
    CLIENT_API_ENDPOINT = "http://localhost/api/v1/get-prediction-scores"
    CLIENT_API_SUPER_KEY = "ABCDEFG"

    @staticmethod
    def model_list(model_type):
        models_dir = os.path.join(os.environ['MODELS_DIRECTORY'], model_type)
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        return [ path.replace("model_", "").replace(".vec", "") \
                 for path in os.listdir(os.path.join(os.environ['MODELS_DIRECTORY'], model_type)) if path.endswith(".vec")]
    
    @staticmethod
    def subreddit_list():
        return CrossmodConsts.model_list("subreddit-clfs")
    
    @staticmethod
    def norm_list():
        return CrossmodConsts.model_list("norm-clfs")
    
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
