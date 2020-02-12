<<<<<<< HEAD
## Code base for *Crossmod: A Cross-Community Learning-based System to Assist Reddit Moderators*

### ACM Reference Format: 
Eshwar Chandrasekharan, Chaitrali Gandhi, Matthew Wortley Mustelier, and Eric Gilbert. 2019. Crossmod: A
Cross-Community Learning-based System to Assist Reddit Moderators. Proc. ACM Hum.-Comput. Interact., CSCW.

### Code directory: 

**code/** - contains the codebase for the system:
  * *crossmod.py*: system code that creates a bot moderator for the test subreddit, taking moderations actions based on the configuration file.
  * *config.py*: configuration file that allows mods to control the system using **IFTTT rules**
  * *crossmodclassifiers.py*: runs the classifiers used by Crossmod for cross-community learning
  * *crossmoddb.py*: stores results predicted by Crossmod
  * *crossmodplots.py*: used for generating various plots to measure interesting metrics
  * *crossmoddbupdater.py*: runs in the background to update the database with the current removal status of comments flagged by Crossmod

**data/** - contains the list of subreddits and norm violations that comprise the system's AI back-end.

Contact authors to obtain the ensemble of classifiers for Crossmod's back-end.

## Documentation:
* Documentation for Crossmod can be accessed at http://crossmod.ml
* Dependencies can be installed using the included *requirements.txt*
=======
The page should be available at https://ceshwar.github.io/crossmod/ 
>>>>>>> restructuring-to-web-app
