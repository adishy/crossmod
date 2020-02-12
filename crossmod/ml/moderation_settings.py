import crossmod
from crossmod.helpers.consts import CrossmodConsts

#IFTTT format - if <condition>: then <action>

def check_config(comment):
	###Configuration file for Crossmod
	
	### below this are the rules that are configured by the moderators
	remove = "remove"
	report = "report"
	modmail = "modmail"

	### initialization
	ACTION = "EMPTY"

	### below this are the rules that are configured by the moderators
	print(comment)

	###conditional statements - to be modified by mods
	try:
		if comment['agreement_score'] >= CrossmodConsts.AGREEMENT_SCORE_THRESHOLD: 
			ACTION = report
	
	### above this are the rules that are configured by the moderators


	except:
		print("missing value!")

	return ACTION