# AEFContentCheck.py

from AEFSubmissionCheck import AEFSubmissionCheck
from AEFAuthorizationsCheck import AEFAuthorizationsCheck
from AEFActionsCheck import AEFActionsCheck
from AEFHoldingsCheck import AEFHoldingsCheck
from AEFAuthEntitiesCheck import AEFAuthEntitiesCheck


class AEFContentCheck:

	def __init__(self):
		self.sheet_count =	7
		self.sheet_names =	[
								"Index",
								"Summary information",
								"Table 1 Submission",
								"Table 2 Authorizations",
								"Table 3 Actions",
								"Table 4 Holdings",
								"Table 5 Auth. entities"
							]


	def check(self, worksheets, field_names):

		is_valid	= True
		submission_check	= AEFSubmissionCheck(worksheets[2], field_names[0])
		if (submission_check.check_content()) is False:
			is_valid	= False
		authorizations_check	= AEFAuthorizationsCheck(worksheets[3], field_names[1])
		if (authorizations_check.check_content()) is False:
			is_valid	= False
		actions_check	= AEFActionsCheck(worksheets[4], field_names[2])
		if (actions_check.check_content()) is False:
			is_valid	= False
		holdings_check	= AEFHoldingsCheck(worksheets[5], field_names[3])
		if (holdings_check.check_content()) is False:
			is_valid	= False
		auth_entities_check	= AEFAuthEntitiesCheck(worksheets[6], field_names[4])
		if (auth_entities_check.check_content()) is False:
			is_valid	= False

		return is_valid

