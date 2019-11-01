import os

class CrossmodConsts:
    PERSPECTIVE_API_SECRET = os.environ['PERSPECTIVE_API_SECRET']
    REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
    REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']

def main():
    print("Perpective API Key: ",      CrossmodConsts.PERSPECTIVE_API_SECRET)
    print("Reddit Client UserAgent:", CrossmodConsts.REDDIT_USER_AGENT)
    print("Reddit Client ID: ",        CrossmodConsts.REDDIT_CLIENT_ID)
    print("Reddit Client Secret",      CrossmodConsts.REDDIT_CLIENT_SECRET)
    print("Reddit Password: ",         CrossmodConsts.REDDIT_PASSWORD)
    print("Reddit Username: ",         CrossmodConsts.REDDIT_USERNAME)

if __name__ == "__main__":
    main()