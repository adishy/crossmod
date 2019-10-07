## Code base for *Crossmod: A Cross-Community Learning-based System to Assist Reddit Moderators*

### ACM Reference Format: 
Eshwar Chandrasekharan, Chaitrali Gandhi, Matthew Wortley Mustelier, and Eric Gilbert. 2019. Crossmod: A
Cross-Community Learning-based System to Assist Reddit Moderators. Proc. ACM Hum.-Comput. Interact., CSCW.

### Code directory: 

**code/** - contains the codebase for the system:
  * *config.py*: configuration file that allows mods to control the system using **IFTTT rules**
  * *getPrediction.py*: modules to query back-end models in order to score incoming comments
  * *crossmod.py*: system code that creates a bot moderator for the test subreddit, taking moderations actions based on the configuration file.

**data/** - contains the list of subreddits and norm violations that comprise the system's AI back-end.

Contact authors to obtain the ensemble of classifiers for Crossmod's back-end.

# Installation instructions:

* Crossmod depends on flask, pandas, praw (python reddit api wrapper) and the google api python client 
  [(Preferably use a virtual environment)](https://realpython.com/python-virtual-environments-a-primer/)
```
pip3 install flask
pip3 install pandas     
pip3 install praw  
pip3 install google-api-python-client
```