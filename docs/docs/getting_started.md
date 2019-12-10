## Installing Crossmod

## Installing Dependencies

* Crossmod is written using Python 3 and has the following dependencies:

* `pandas` (Python Data Analysis Library)
* `praw` (Python Reddit API Wrapper)
* `google-api-client` (Python Google API Client)
* `flask` (Flask Web Framework)
* `sqlalchemy` (Object Relational Mapping interface for database)
* `fasttext` (Python wrapper for fasttext binaries)
* `seaborn` (Used for styling plots)

* Install these dependencies by running the following commands:
  ```
  pip3 install flask
  pip3 install pandas
  pip3 install praw
  pip3 install google-api-python-client
  pip3 install sqlalchemy
  pip3 install fasttext
  pip3 install seaborn
  ```
Note that using a Python virtual environment is highly recommended (but not necessary). A guide to set up a Python virtual environment can be found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/).
If using a python virtual environment, replace `pip3` with `pip` when installing Crossmod dependencies. 

Getting Credentials for Crossmod

* Crossmod currently uses Google’s Perspective API for moderation tasks. 
A personal Perspective API Key can be obtained following [these instructions](https://github.com/conversationai/perspectiveapi/tree/master/1-get-started). After obtaining the API key, paste it into `crossmod_credentials.sh` as described below.
* Obtain Reddit API credentials by creating an app [here](https://www.reddit.com/prefs/apps) and paste the client ID and client secret along with the username and password for the Reddit account used for creating the app in `crossmod credentials.sh` as described below.

## Set up keys

* Crossmod depends on a few credentials and constants, such as the key for Perspective API, Reddit credentials for `praw`, and the paths to the sqlite database file and the Crossmod fasttext classifiers.

* To set up the keys file for Crossmod, first cp the crossmod_credentials_example.sh to a file called crossmod_credentials.sh
Assuming the Crossmod repository was cloned to the home directory of the user

~~~
    git clone https://github.com/ceshwar/crossmod
    cd crossmod
    cp crossmod_credentials_example.sh crossmod_credentials.sh
~~~

* Open crossmod_credentials.sh and replace the keys with credentials obtained previously. The crossmod_credentials.sh file should also contain the path to the directory containing fasttext models that Crossmod requires for cross-community predictions.
* `PERSPECTIVE_API_SECRET` is the API key for Perspective API
* `REDDIT_USER_AGENT` is the User-Agent value for Crossmod, this can be set to any value that makes sense, for example, "Testing Crossmod (by /u/CrossModerator)"
* `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` are obtained by [creating an app]() on Reddit as described previously.  

* `REDDIT_PASSWORD`, `REDDIT_USERNAME` are the password and the username of the Reddit account that was used to obtain the API credentials

* `MODELS_DIRECTORY` is the path to fasttext classifiers required by Crossmod

* A complete `crossmod_credentials.sh` file looks like this:
~~~
export PERSPECTIVE_API_SECRET=GFDKHJN43jkngrjkegbjkbgfdkj
export REDDIT_USER_AGENT="Testing Crossmod (by /u/CrossModerator)"
export REDDIT_CLIENT_ID=s-GFKNGlngkfd
export REDDIT_CLIENT_SECRET=JBGFDJLGDFGJ
export REDDIT_PASSWORD=your_password_for_reddit
export REDDIT_USERNAME=YourUsernameForReddit
export MODELS_DIRECTORY="/models/directory"
~~~

* Edit ~/.profile to load Crossmod credentials into the environment on login
~~~
    echo "source ~/crossmod/crossmod_credentials.sh" >> ~/.profile
    source ~/.profile
~~~

## Starting Crossmod
* Crossmod can be started by running the `crossmod.py` script with the required arguments:
    * The name of the subreddit
    * An indicator to actually perform actions specified in config.py [0, 1]
    * An indicator to use Crossmod's backend classifers [0, 1]
~~~
    cd ~/crossmod/code
    # crossmod.py <subreddit-name> <perform-action [0, 1]> <use-classifiers [0, 1]>
    python3 crossmod.py modbot_staging 1 1
~~~


