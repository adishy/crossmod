## Code base for *Crossmod: A Cross-Community Learning-based System to Assist Reddit Moderators*

### ACM Reference Format: 
Eshwar Chandrasekharan, Chaitrali Gandhi, Matthew Wortley Mustelier, and Eric Gilbert. 2019. Crossmod: A
Cross-Community Learning-based System to Assist Reddit Moderators. Proc. ACM Hum.-Comput. Interact., CSCW.

### Code directory: 
* crossmod: A package that provides interfaces to all of Crossmod's services
* Crossmod can be run as an API service and can also be run as a command line tool

Contact authors to obtain the ensemble of classifiers for Crossmod's back-end.

## Installing Crossmod:
```bash
# Install Python pip and venv and other dependencies
sudo apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv

# Clone the repository
git clone http://github.com/ceshwar/crossmod

# Create a virtual environment (Crossmod requires Python 3.6 or higher)
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install the Crossmod package locally
pip install -e .

# Make sure you have credentials set up as specified in the docs
# The environment variables specified in crossmod_credentials_example.sh should be
# available in the shell that Crossmod runs in

# To use Crossmod to moderate subreddits, first start the API service
crossmod api &

# Then start the Crossmod subreddit monitor
crossmod monitor 
```
## Documentation:
* Documentation for Crossmod can be accessed at http://crossmod.ml/docs
