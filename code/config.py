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
		if comment['toxicity_score'] >= 0.9: 
			ACTION = remove
		elif comment['agreement_score'] >= 85: 
			ACTION = report
		elif comment['prediction_science'] == True:
			ACTION = report
		elif comment['agreement_score'] >= 90 and comment['prediction_The_Donald'] == False:
			ACTION = remove
		elif comment['prediction_hatespeech-racist-homophobic'] == True and comment['norm_violation_score'] >= 6: 
			ACTION = report
		elif comment['prediction_misogynistic-slurs'] == True and comment['prediction_personal-attacks'] == True: 
			ACTION = modmail
	
	### above this are the rules that are configured by the moderators


	except:
		print("missing value!")

	return ACTION