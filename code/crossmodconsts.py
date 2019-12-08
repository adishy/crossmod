import os

class CrossmodConsts:
    PERSPECTIVE_API_SECRET = os.environ['PERSPECTIVE_API_SECRET']
    REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
    REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']

    FASTTEXT_BINARY = "../../fastText-0.9.1/fasttext"
    MODELS_DIRECTORY = os.environ['MODELS_DIRECTORY']

    SUBREDDIT_CLASSIFIERS = "subreddit"
    NORM_CLASSIFIERS = "norms"

    @staticmethod
    def get_norms_classifier(norm):
        NORMS_CLASSIFIERS = CrossmodConsts.MODELS_DIRECTORY + "/norm-clfs/"
        return NORMS_CLASSIFIERS + "model_" + norm + ".bin"

    @staticmethod
    def get_subreddit_classifier(subreddit):
        SUBREDDIT_CLASSIFIERS = CrossmodConsts.MODELS_DIRECTORY + "/subreddit-clfs/"
        return SUBREDDIT_CLASSIFIERS + "model_" + subreddit + ".bin"

    @staticmethod
    def get_classifier(clf_id, type):
        if type == CrossmodConsts.SUBREDDIT_CLASSIFIERS:
            return CrossmodConsts.get_subreddit_classifier(clf_id)
        elif type == CrossmodConsts.NORM_CLASSIFIERS:
            return CrossmodConsts.get_norms_classifier(clf_id)
        
        raise RuntimeError("Could not find classifier: ", clf_id, " of type: ", type)

def main():
    print("Perpective API Key: ",      CrossmodConsts.PERSPECTIVE_API_SECRET)
    print("Reddit Client UserAgent:",  CrossmodConsts.REDDIT_USER_AGENT)
    print("Reddit Client ID: ",        CrossmodConsts.REDDIT_CLIENT_ID)
    print("Reddit Client Secret",      CrossmodConsts.REDDIT_CLIENT_SECRET)
    print("Reddit Password: ",         CrossmodConsts.REDDIT_PASSWORD)
    print("Reddit Username: ",         CrossmodConsts.REDDIT_USERNAME)

    print("fastText binary: ",         CrossmodConsts.FASTTEXT_BINARY)
    print("Norms model: ",             CrossmodConsts.get_norms_classifier('verbal-attacks-on-Reddit'))
    print("Subreddit model: ",         CrossmodConsts.get_subreddit_classifier('Futurology'))

if __name__ == "__main__":
    main()
