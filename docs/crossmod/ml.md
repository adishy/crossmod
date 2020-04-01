## Machine Learing Models

Crossmod is currently using [Fasttext](https://github.com/facebookresearch/fastText) as its backend model. 

### Data Training

Now we have 100 models that were trained on 100 subreddits on Reddit and 8 models that were trained on Macro Norm. These models are pre-trained by the data we collected before. We would use the predication from all of them and take actions according to user's manual configuration.

### Data Prediction

The main prediction process is `subreddit_monitor.py`. It could listen to mulitple subreddits and take actions on some of them. The list could be changed in the database. The main steps are:

1. Crossmod will use [praw](https://praw.readthedocs.io/en/latest/) to fetch comments in mulitple subreddits;
2. Then it will check the whitelisted option and also filtered the comments by `helpers/filters.py` (which could get rid of links, emojis and other symbols that could not be used for detecting violations)
3. Then it will use our [API](https://ceshwar.github.io/crossmod/crossmod/api/) service to use our backend models to get the prediction. It will generate two scores `agreement_score` from 100 subreddit models and `norm_violation_score` from 8 macro norm models. 
4. Crossmod will store the data into database. It could do retraining and data analysis with these data in the future.
5. (Optional) If the user chooses to take action on the subreddit of this comment, crossmod will use [praw](https://praw.readthedocs.io/en/latest/) to report it to the moderators on Reddit.

### Data Retraining

Because we have collected many comments from different subreddits, we could do data retraining to improve the accuracy of our backend model. Our plan is:

1. We could use our new data to train a new subreddit model and add it to our model list.