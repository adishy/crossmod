

## Quick Start
 ### Running a local instance
* Clone Crossmoderator repository
	* [https://github.com/ceshwar/crossmod](https://github.com/ceshwar/crossmod)
* Install dependencies

```
./bin/crossmod_flask_run.sh
```

##### Flask (Outdated)

```Console
$ export FLASK_APP=api.py
$ flask run --host=0.0.0.0 -p 6000
```
##### Gunicorn (Outdated)
```Console
$ gunicorn3 --bind 0.0.0.0:6000 wsgi
```

## API Request Format
An API request takes the following format:
```
http://crossmod.ml/api/v1/get-prediction-scores
```
The API call request is a JSON object with the following fields:

    {
        "comments": [ comment1, comment2, ... ],
        "subreddit_list": [ classifier1, classifier2, ... ],
        "macro_norm_list": [ norm1, norm2, ... ],
        "key": KEY
    }


* `comments: ` array of comment strings to be evaluated
* `subreddit_list [OPTIONAL]: ` list of subreddit classifiers used to predict scores.
    * If field is left blank, all default classifiers in ../data/study_subreddits.csv will all be used
    * If field is passed a blank list [], no classifiers will be used, and no  agreement score will be found
* `macro_norm_list [OPTIONAL]:` list of macro norms used to predict scores.
        * If field is left blank, all default macro norms in ../data/macro-norms.txt will all be used
        * If field is passed a blank list [], no macro norms will be used, and no norm violation score will be found
* `key`: string used for authentication.
        * currently, for debugging, key is set to `ABCDEFG`

### Sample API Requests
Examples of API requests made through command line with cURL:

<sub>Rating comments with all classifiers and no macro norms</sub>
```bash
    $ curl -d '{"comments": ["you really suck!", "this is just a comment"], "macro_norm_list": [], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://crossmod.ml/api/v1/get-prediction-scores
```

<sub>Rating comments with only select classifiers and all macro norms</sub>
```
    $ curl -d '{"comments": ["you really suck!", "this is just a comment"], "subreddit_list": ["Futurology", "nba", "AskReddit", "science", "politics", "pokemongo"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://crossmod.ml/api/v1/get-prediction-scores
```

<sub>Rating comments with all classifiers and all macro norms</sub>
```
    $ curl -d '{"comments": ["you really suck!", "this is just a comment"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://crossmod.ml/api/v1/get-prediction-scores
```
For examples of making API calls through Python, see `api_demo.py`.

## Responses

* The API response is an array of JSON objects, where the index of each JSON object  corresponds to the index of the original comment in the request.

  ```
    [
        {
            'agreement_score': AGREEMENT_SCORE,
            'norm_violation_score': NORM_VIOLATION_SCORE,
            'subreddits_that_remove': [ subreddit1, subreddit2, ... ],
            'norms_violated': [ norm1, norm2, ... ]
        },
        ....
    ]
   ```
 * `agreement_score:` prediction score from subreddit classifiers. If no classifiers were used, is a `NULL` value.
  * `norm_violation_score: ` prediction score from macro norms. If no macro norms were used, is a `NULL` value.
   * `subreddits_that_remove: ` list of classifiers that voted to removed the comment. If no classifiers were used, is an `empty` list.
    * `norms_violated: ` list of norms that were violated by the comment. If no macro norms were used, is an `empty` list.




## Local Instance Dependencies
Again, if you run a local instance of the API, a virtual environment is recommended.
```
 crossmodclassifiers.py
 flask
 pandas
 traceback
 json
```
  To deploy with Gunicorn:
```
 wsgi.py
 gunicorn3
```

## Troubleshooting
 **If an API response contains:**
```
[Errno 12] Cannot allocate memory
```
the server is experiencing memory issues. Crossmod may be experiencing memory leaks.

**If there is a port conflict when running a local instance:**
try switching from port 6000 to an alternative port such as 8000.
