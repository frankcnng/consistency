# AEFSummaryCheck.py
#
# Checks the Summary worksheet:
# - ensures the field names in the Summary sheet match those in the Constructor
#

import AEFColumnFieldsSyntaxCheck
import syntaxreport


class AEFSummaryCheck(AEFColumnFieldsSyntaxCheck):

	def __init__(self):
		self.template_sheet_name	= "Summary information"
		self.submission_fields		=	[
											"Table 1: Submission",
											"Party",
											"Version",
											"Reported year",
											"Date of submission",
											"Review status of the initial report",
											"Result of the consistency check of this AEF submission",
											"First year of the NDC implementation period",
											"Last year of the NDC implementation period",
											"Reference to the Article 6 technical expert review report of the initial report"
										]
		self.authorizations_fields =	[
											"Table 2: Authorizations",
											"Authorization ID",
											"Date of authorization",
											"Cooperative approach ID",
											"Version of the authorization",
											"Authorized quantity",
											"Metric",
											"Applicable GWP value(s)",
											"Applicable non-GHG metric",
											"Sector(s)",
											"Activity type(s)",
											"Purposes for authorization",
											"Authorized Party(ies) ID",
											"Authorized entity(ies) ID",
											"OIMP authorized by the Party",
											"Authorized timeframe",
											"Authorization terms and conditions",
											"Authorization documentation",
											"First transfer definition for OIMP",
											"Additional explanatory information"
										]
		self.actions_fields			=	[
											"Table 3: Actions",
											"Action date",
											"Action type",
											"Action subtype",
											"Cooperative approach ID",
											"Authorization ID",
											"First transferring participating Party ID",
											"Party ITMO registry ID",
											"First ID",
											"Last ID",
											"Underlying unit registry ID",
											"First unit ID",
											"Last unit ID",
											"Metric",
											"Applicable GWP value(s)",
											"Applicable non-GHG metric",
											"Quantity (t CO2 eq)",
											"Quantity (in non-GHG metric)",
											"Mitigation type",
											"Vintage",
											"Transferring participating Party ID",
											"Acquiring participating Party ID",
											"Purpose for which the ITMO has been used towards or cancelled for OIMP",
											"Using/cancelling participating Party ID",
											"Using/cancelling authorized entity ID",
											"Calendar year for which the ITMOs are used towards the Party's NDC",
											"Result of the consistency checks",
											"Additional explanatory information"
										]
		self.holdings_fields		=	[
											"Table 4: Holdings",
											"Cooperative approach ID",
											"Authorization ID",
											"First transferring participating Party ID",
											"Party ITMO registry ID",
											"First ID",
											"Last ID",
											"Underlying unit registry ID",
											"First unit ID",
											"Last unit ID",
											"Metric",
											"Applicable GWP value(s)",
											"Applicable non-GHG metric",
											"Quantity (t CO2 eq)",
											"Quantity (in non-GHG metric)",
											"Mitigation type",
											"Vintage"
										]
		self.auth_entities_fields	=	[
											"Table 5: Authorized entities",
											"Date of the authorization",
											"Name",
											"Country of incorporation",
											"Identification number",
											"Cooperative approach ID",
											"Conditions",
											"Change and revocation conditions",
											"Additional explanatory information"
										]


	def check_structure(self, workbook, field_names, check_report):
		sheet_report	= syntaxreport.AEFCheckSheetReport(self.template_sheet_name)
		check_report.add_sheet_report(sheet_report)
#		str_results[0]	+= "\n\tChecking the structure of '" + self.template_sheet_name + "'"

		self.set_field_names(field_names)
		dest_names	= workbook.sheetnames
		worksheet	= None
		for dest_name in dest_names:
			if dest_name == self.template_sheet_name:
				worksheet 		= workbook[dest_name]
				self.worksheet	= worksheet
				break
		if (worksheet == None):
			cell_report	= syntaxreport.AEFCheckCellReport(None, "Could not find worksheet '" + self.template_sheet_name + "'.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\tCould not find worksheet '" + self.template_sheet_name + "'."

		for x_table in range (0, 4):
			self.field_names	= field_names[x_table]
			if (self.check_field_names(check_report)) is False:
				return False
		return True


	def set_field_names(self, field_names):
		field_names.append(self.submission_fields)
		field_names.append(self.authorizations_fields)
		field_names.append(self.actions_fields)
		field_names.append(self.holdings_fields)
		field_names.append(self.auth_entities_fields)

