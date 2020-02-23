from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.helpers.consts import CrossmodConsts

clf_ensemble = CrossmodClassifiers(subreddits = CrossmodConsts.SUBREDDIT_LIST,
                                   norms = CrossmodConsts.NORM_LIST)