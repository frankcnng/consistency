# AEFContentCheck.py

# from AEFSubmissionCheck import AEFSubmissionCheck
# from AEFAuthorizationsCheck import AEFAuthorizationsCheck
# from AEFActionsCheck import AEFActionsCheck
# from AEFHoldingsCheck import AEFHoldingsCheck
# from AEFAuthEntitiesCheck import AEFAuthEntitiesCheck

import aefsheets
from syntaxreport.AEFSheetReport import AEFSheetReport


class AEFContentCheck:

	def check(self, worksheets, field_names, check_report):
		check_report.add_sheet_report(AEFSheetReport("Content check", 2))
		is_valid			= True
		submission_check	= aefsheets.AEFSubmission(worksheets[2], field_names[0])
		if (submission_check.check_content(check_report)) is False:
			is_valid	= False
		authorizations_check	= aefsheets.AEFAuthorizations(worksheets[3], field_names[1])
		if (authorizations_check.check_content(check_report)) is False:
			is_valid	= False
		actions_check	= aefsheets.AEFActions(worksheets[4], field_names[2])
		if (actions_check.check_content(check_report)) is False:
			is_valid	= False
		holdings_check	= aefsheets.AEFHoldings(worksheets[5], field_names[3])
		if (holdings_check.check_content(check_report)) is False:
			is_valid	= False
		auth_entities_check	= aefsheets.AEFAuthEntities(worksheets[6], field_names[4])
		if (auth_entities_check.check_content(check_report)) is False:
			is_valid	= False

		return is_valid

