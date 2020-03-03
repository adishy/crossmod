import crossmod
from crossmod.environments.consts import CrossmodConsts

#IFTTT format - if <condition>: then <action>

def check_config(comment):
	###Configuration file for Crossmod
	
	### below this are the rules that are configured by the moderators
	remove = "remove"
	report = "report"
	modmail = "modmail"

	### initialization
	ACTION = "EMPTY"

	###conditional statements - to be modified by mods
	try:
		if comment['agreement_score'] >= CrossmodConsts.AGREEMENT_SCORE_THRESHOLD: 
			ACTION = report
	
	### above this are the rules that are configured by the moderators


	except:
		print("missing value!")

	return ACTION
