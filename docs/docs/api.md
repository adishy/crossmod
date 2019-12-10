## Quick Start
* install DEPENDENCIES
* Navigate to crossmod_api/code
```~
export FLASK_APP=api.py
flask run
```~
## Requests

* The JSON request is an object with the following fields:
```
    {
        "comments": [ comment1, comment2, ... ],
        "subreddit_list": [ classifier1, classifier2, ... ],
        "macro_norm_list": [ norm1, norm2, ... ],
        "key": KEY
    }
```

* `comments: ` array of comment strings to be evaulated by Crossmod
* `subreddit_list: ` (OPTIONAL) list of subreddit classifiers used to predict scores.
    * If field is left blank, the default classifiers in ../data/study_subreddits.csv will all be used
    * If field is passed a blank list [], no classifiers will be used, and no  agreement score will be found
* `macro_norm_list: ` (OPTIONAL) list of macro norms used to predict scores.
        * If field is left blank, the default macro norms in ../data/macro-norms.txt will all be used
        * If field is passed a blank list [], no macro norms will be used, and no norm violation score will be found
* `key`: string used for authentication.
        * currently, for debugging, key is set to `ABCDEFG`
    
## Example Requests
* While flask is running:
    * rating comments with all classifiers and no macro norms

```bash
    curl -d '{"comments": ["you really suck!", "this is just a comment"], "macro_norm_list": [], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores
```
    
    * rating comments with only select classifiers and all macro norms
    
```
    curl -d '{"comments": ["you really suck!", "this is just a comment"], "subreddit_list": ["Futurology", "nba", "AskReddit", "science", "politics", "pokemongo"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores
```

    * rating comments with all classifiers and all macro norms

```
    curl -d '{"comments": ["you really suck!", "this is just a comment"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores
```

## Responses

* The JSON response is an array of JSON objects, where the index of each JSON object
  corresponds to the index of the original comment in the request.

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

    * `agreement_score: ` prediction score from subreddit classifiers.
        * if no classifiers were used, is a `NULL` value.
    * `norm_violation_score: ` prediction score from macro norms.
        * if no macro norms were used, is a `NULL` value.
    * `subreddits_that_remove: ` list of classifiers that would have removed the comment.
        * if no classifiers were used, is an empty list
    * `norms_violated: ` list of norms that were violated by the comment.
        * if no macro norms were used, is an empty listed
    * CHECK IF agreement_score OR norm_violation_score IS NULL
            NOT IF subreddits_that_remove OR norms_violated IS EMPTY
             because a NULL value implies that classifiers and/or macro norms were not used
             whereas an EMPTY list does NOT NECESSARILY imply the above

## Dependencies
    * `getPredictions.py`
    * `flask`
    * `pandas`
    * `traceback`
    * `json`

## Common Troubleshooting
    * Make sure getPredictions.py points to the correct paths for the norm/reddit models and the fastText directory
    * Make sure fastText binaries are compiled on local machine.
        * If not, navigate to `/fastText-0.9.1` and `make clean && make`
