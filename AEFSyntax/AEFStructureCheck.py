# AEFStructureCheck.py

# import AEFSummaryCheck
# import AEFSubmissionCheck
# import AEFAuthorizationsCheck
# import AEFActionsCheck
# import AEFHoldingsCheck
# import AEFAuthEntitiesCheck

import aefsheets

from syntaxreport.AEFSheetReport import AEFSheetReport
from syntaxreport.AEFCellReport import AEFCellReport


class AEFStructureCheck:
	"""Checks the structure of an AEF workbook.
	Check the number of sheets.
	Check the names of the sheets.
	Check each sheet for the correct field headings.
	"""

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


	def check(self, workbook, worksheets, field_names, check_report):
		if (self.check_sheet_count(workbook, check_report)) is False:
			return False
		if (self.check_sheet_names(workbook, worksheets, check_report)) is False:
			return False
		return (self.check_sheets(workbook, worksheets, field_names, check_report))


	def check_sheet_count(self, workbook, check_report):
		sheet_report	= AEFSheetReport("Check sheet count")
		check_report.add_sheet_report(sheet_report)
		if (len(workbook.sheetnames) != (self.sheet_count)):
			cell_report	= AEFCellReport(None, "Incorrect number of worksheets in workbook")
			sheet_report.add_cell_report(cell_report)
			return False
		else:
			cell_report	= AEFCellReport(None, "Correct number of worksheets in workbook.")
			sheet_report.add_cell_report(cell_report)
			return True


	def check_sheet_names(self, workbook, worksheets, check_report):
		dest_names		= workbook.sheetnames
		for source_name in self.sheet_names:
			sheet_report	= AEFSheetReport(source_name)
			check_report.add_sheet_report(sheet_report)
			if (source_name in dest_names) is False:
				cell_report	= AEFCellReport(None, "The worksheet '" + source_name + "'' was not found.")
				sheet_report.add_cell_report(cell_report)
				return False
			else:
				worksheets.append(workbook[source_name])
		sheet_report	= AEFSheetReport("")
		check_report.add_sheet_report(sheet_report)
		cell_report	= AEFCellReport(None, "All workseets found in workbook.")
		sheet_report.add_cell_report(cell_report)
		return True


	def check_sheets(self, workbook, worksheets, field_names, check_report):
		is_valid	= True
		summary_check	= aefsheets.AEFSummary()
		if (summary_check.check_structure(workbook, field_names, check_report)) is False:
			is_valid	= False
		submission_check	= aefsheets.AEFSubmission(worksheets[2], field_names[0])
		if (submission_check.check_structure(check_report)) is False:
			is_valid	= False
		authorizations_check	= aefsheets.AEFAuthorizations(worksheets[3], field_names[1])
		if (authorizations_check.check_structure(check_report)) is False:
			is_valid	= False
		actions_check	= aefsheets.AEFActions(worksheets[4], field_names[2])
		if (actions_check.check_structure(check_report)) is False:
			is_valid	= False
		holdings_check	= aefsheets.AEFHoldings(worksheets[5], field_names[3])
		if (holdings_check.check_structure(check_report)) is False:
			is_valid	= False
		auth_entities_check	= aefsheets.AEFAuthEntities(worksheets[6], field_names[4])
		if (auth_entities_check.check_structure(check_report)) is False:
			is_valid	= False
		return is_valid
