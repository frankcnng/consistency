# AEFStructure.py

from AEFSummaryCheck import AEFSummaryCheck
from AEFSubmissionCheck import AEFSubmissionCheck
from AEFAuthorizationsCheck import AEFAuthorizationsCheck
from AEFActionsCheck import AEFActionsCheck
from AEFHoldingsCheck import AEFHoldingsCheck
from AEFAuthEntitiesCheck import AEFAuthEntitiesCheck


class AEFStructure:

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


	def check(self, workbook, worksheets, field_names):
		if (self.check_sheet_count(workbook)) is False:
			return False
		if (self.check_sheet_names(workbook, worksheets)) is False:
			return False
		summary_check	= AEFSummaryCheck()
		if (summary_check.check_structure(workbook, field_names)) is False:
			return False
		submission_check	= AEFSubmissionCheck(worksheets[2], field_names[0])
		if (submission_check.check_structure()) is False:
			return False
		authorizations_check	= AEFAuthorizationsCheck(worksheets[3], field_names[1])
		if (authorizations_check.check_structure()) is False:
			return False
		actions_check	= AEFActionsCheck(worksheets[4], field_names[2])
		if (actions_check.check_structure()) is False:
			return False
		holdings_check	= AEFHoldingsCheck(worksheets[5], field_names[3])
		if (holdings_check.check_structure()) is False:
			return False
		auth_entities_check	= AEFAuthEntitiesCheck(worksheets[6], field_names[4])
		if (auth_entities_check.check_structure()) is False:
			return False
		return True


	def check_sheet_count(self, workbook):
		return (len(workbook.sheetnames) == self.sheet_count)


	def check_sheet_names(self, workbook, worksheets):
		dest_names		= workbook.sheetnames
		for source_name in self.sheet_names:
			if (source_name in dest_names) is False:
				print ("The worksheet '" + source_name + "'' was not found in the workbook.")
				return False
			else:
				worksheets.append(workbook[source_name])
		return True
