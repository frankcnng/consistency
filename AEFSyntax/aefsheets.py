# aefsheets.py

from openpyxl.comments import Comment
import re

from syntaxreport.AEFSheetReport import AEFSheetReport
from syntaxreport.AEFCellReport import AEFCellReport


class AEFSheet:
	"""Abstract superclass that checks the syntax of a worksheet."""

	def __init__(self, worksheet, field_names):
		self.worksheet		= worksheet
		self.field_names	= field_names


	def check_structure(self, check_report):
		sheet_report	= AEFSheetReport(self.template_sheet_name)
		check_report.add_sheet_report(sheet_report)
#		str_results[0]	+= "\n\tChecking the structure of '" + self.template_sheet_name + "'"
		return self.check_field_names(sheet_report)


	def check_field_names(self, sheet_report):
		return True


	def check_content(self, sheet_report):
		return True
	

	def check_cell_content(self, x_target_row, x_target_column, x_tuple, sheet_report):
		field_reg_exp_tuple	= self.field_reg_exp_tuples[x_tuple]
		field_name			= field_reg_exp_tuple[0]
		field_reg_exp		= field_reg_exp_tuple[1]

		if (field_reg_exp == ""):
			return True

		field_error_mesg	= field_reg_exp_tuple[2]
		cell				= self.worksheet.cell(x_target_row, x_target_column)
		if (re.match("^blankable", field_reg_exp) != None):	# if the cell can be either blank, of a defined set of values
			if (cell.value == None):	# if the cell is empty
				return True

		if (cell.data_type == 'd'):
			if (re.match(field_reg_exp, str(cell.number_format)) == None):
				str_message	= "Cell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy"
				self.add_comment(cell, str_message)
				str_link	= "#'" + self.template_sheet_name + "'" + "!" + self.coord2cell_ref(x_target_row, x_target_column)
				cell_report	= AEFCellReport(str_link, str_message)
				sheet_report.add_cell_report(cell_report)
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:
			str_message	= "Cell content error: The value provided for '" + field_name + field_error_mesg
			self.add_comment(cell, str_message)
			str_link	= "#'" + self.template_sheet_name + "'" + "!" + self.coord2cell_ref(x_target_row, x_target_column)
			cell_report	= AEFCellReport(str_link, str_message)
			sheet_report.add_cell_report(cell_report)
			return False
		return True

	def add_comment(self, cell, str_comment):
		comment	= Comment(str_comment, "AEFSyntaxCheck")
		cell.comment	= comment


	def coord2cell_ref(self, x_row, x_column):
		# return the alpha number excel cell reference from row number and column number (1-based)
		if (x_column <= 26):
			return (chr(ord('A') + x_column - 1) + str(x_row))
		else:
			return ("A" + chr(ord('A') + (x_column % 26) - 1) + str(x_row))


class RowFieldsSheet(AEFSheet):
	"""Abstract superclass for checks syntax of worksheets with fields organised in rows."""

	def check_field_names(self, sheet_report):
	# Check the names of the field names (headings) in the sheet correspond with those in the field_names array
	#
		heading_column		= 0
		fields_start_column	= 0
		fields_end_column	= 0
		field_headings_row	= 0
		template_fields		= self.field_names
		n_template_fields	= len(template_fields)
		worksheet			= self.worksheet
		for column in worksheet.iter_rows(min_row=worksheet.min_row, max_row=worksheet.max_row, min_col=worksheet.min_column, max_col=worksheet.max_column):
			if (field_headings_row > 0):
				break
			else:
				n_blank_cells	= 0
			for cell in column:
				if ((cell.data_type == "s") and (cell.value.casefold() == template_fields[0].casefold())):
					heading_column	= cell.column
					continue
				elif ((heading_column > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[1].casefold())):
					fields_start_column	= cell.column
					field_headings_row	= cell.row
					continue
				elif (fields_start_column > 0):
					if (cell.row == field_headings_row):
						if ((cell.value == None)):
							n_blank_cells	= n_blank_cells + 1
							continue
						elif ((fields_start_column > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[n_template_fields - 1].casefold())):
							fields_end_column	= cell.column
							break
					else:
						break

		str_link	= "#" + self.template_sheet_name + "!A1"
		if (heading_column == 0):
			cell_report	= AEFCellReport(str_link, "Could not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet."
			return False
		elif (fields_start_column == 0):
			cell_report	= AEFCellReport(str_link, "Could not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet."
			return False
		elif (fields_end_column == 0):
			cell_report	= AEFCellReport(str_link, "Could not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] +"' worksheet."
			return False
		elif ((fields_end_column - fields_start_column - n_blank_cells + 1) != (n_template_fields - 1)):	# (n_template_fields - 1) as the first element of array is sheet name
			cell_report	= AEFCellReport(str_link, "Could not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tNumber of fields in '" + template_fields[0] + "' worksheet is incorrect."
			return False

		dest_fields	= []
		for column in worksheet.iter_rows(min_col=fields_start_column, max_col=fields_end_column, min_row=field_headings_row, max_row=field_headings_row, values_only=True):
			dest_fields.append(column)

		for x_field in range (1, n_template_fields):
			if (template_fields[x_field] in dest_fields[0]) is False:
				cell_report	= AEFCellReport(str_link, "The field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet.")
				sheet_report.add_cell_report(cell_report)
#				str_results[0]	+= "\n\t\tThe field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet."
				return False
		return True


	def check_content(self, check_report):
	# Check the contents of the fields in the sheet are syntactically correct
	#
		sheet_report	= AEFSheetReport("Checking the content of '" + self.template_sheet_name + "'")
		check_report.add_sheet_report(sheet_report)
#		str_results[0]	+= "\n\tChecking the content of '" + self.template_sheet_name + "'"

		fields_start_column	= 0
		fields_end_column	= 0
		fields_row			= 0
		template_fields		= self.field_names
		n_template_fields	= len(template_fields)
		worksheet			= self.worksheet
		for column in worksheet.iter_rows(min_row=worksheet.min_row, max_row=worksheet.max_row, min_col=worksheet.min_column, max_col=worksheet.max_column):
			for cell in column:
				if ((cell.data_type == "s") and (cell.value.casefold() == template_fields[1].casefold())):
					fields_start_column	= cell.column
					fields_row			= cell.row
					continue
				elif ((fields_start_column > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[n_template_fields - 1].casefold())):
					fields_end_column	= cell.column
					break

		row			= fields_row + 1	# content is in the row after the field names
		x_tuple		= 0
		is_valid	= True

		for x_column in range(fields_start_column, fields_end_column):
			if (self.check_cell_content(row, x_column, x_tuple, sheet_report)) is False:
				is_valid	= False
			x_tuple	+= 1
		return is_valid


class AEFAuthorizations(RowFieldsSheet):
	"""Concrete subclass for AEF Authorizations worksheet."""

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 2 Authorizations"

		self.field_reg_exp_tuples	=	[
											["Authorization ID", "[A-Za-z0-9 \-]+", "' can only contain alphanumeric, space, and hyphen characters."],
											["Date of authorization", "dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Cooperative approach ID", "CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Version of the authorization", "\d+", "' must be a number."],
											["", "", ""],
											["Authorized quantity", "\d+", "' must be a number."],
											["Metric", "GHG|non\-GHG", "' must 'GHG' or 'non-GHG'"],
											["Applicable GWP value(s)", "", ""],
											["Applicable non-GHG metric", "", ""],
											["Sector(s)", "[A-Za-z0-9 ]+", "' can only contain alphanumeric, and space characters."],
											["Activity type(s)", "[A-Za-z0-9 ]+", "' can only contain alphanumeric, and space characters."],
											["Purposes for authorization", "NDC|OIMP|IMP|OP|NDC and OIMP|NDC and IMP|NDC and OP", "' must be one of 'NDC', 'OIMP', 'IMP', 'OP', 'NDC and OIMP', 'NDC and IMP', or 'NDC and OP'."],
											["Authorized Party(ies) ID", "[A-Z]{3}( *, *[A-Z]{3})*", "' must a comma-separated list of ISO 3166 alpha-3 codes."],
											["Authorized entity(ies) ID", "[A-Za-z0-9 \-]+( *, *[A-Za-z0-9 \-]+)*", "' must a comma-separated list of entity names."],
											["OIMP authorized by the Party", "", ""],
											["Authorized timeframe", "blankable|(\d{4} *\- *\d{4})*", "' must be empty of a year range (dddd - dddd)"],
											["Authorization terms and conditions", "", ""],
											["Authorization documentation", "", ""],
											["First transfer definition for OIMP", "blankable|Authorization|Issuance|Use of cancellation", "' must be empty or one of 'Authorization', 'Issuance', 'Use of cancellation;."],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)


class AEFActions(RowFieldsSheet):
	"""Concrete subclass for AEF Actions worksheet."""

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 3 Actions"

		self.field_reg_exp_tuples	=	[
											["Action date", "dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Action type", "Acquistion|Transfer|Use|Cancellation|First transfer", "'' must be one of 'Acquistion', 'Transfer', 'Use', 'Cancellation', 'First transfer'"],
											["Action subtype", "", ""],
											["Cooperative approach ID", "CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Authorization ID", "[A-Za-z0-9 \-]+", "' can only contain alphanumeric, space, and hyphen characters."],
											["First transferring participating Party ID", "[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Party ITMO registry ID", "[A-Z]{3}\d{2}", "' must be a Party ID followed by two digits"],
											["First ID", "", ""],
											["Last ID", "", ""],
											["", "", ""],
											["Underlying unit registry ID", "", ""],
											["First unit ID", "", ""],
											["Last unit ID", "", ""],
											["", "", ""],
											["Metric", "GHG|non\-GHG", "' must 'GHG' or 'non-GHG'"],
											["Applicable GWP value(s)", "", ""],
											["Applicable non-GHG metric", "", ""],
											["Quantity (t CO2 eq)", "blankable|\d+", "' must be a numerical value."],
											["Quantity (in non-GHG metric)", "blankable|\d*", "' must be a numerical value."],
											["", "", ""],
											["Mitigation type", "", ""],
											["Vintage", "blankable|\d{4}", "' must be a year."],
											["", "", ""],
											["Transferring participating Party ID", "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Acquiring participating Party ID",  "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["", "", ""],
											["Purpose for which the ITMO has been used towards or cancelled for OIMP", "", ""],
											["Using/cancelling participating Party ID", "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Using/cancelling authorized entity ID", "", ""],
											["Calendar year for which the ITMOs are used towards the Party's NDC", "blankable|\d{4}", "' must be a year."],
											["", "", ""],
											["Result of the consistency checks", "", ""],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)


class AEFHoldings(RowFieldsSheet):
	"""Concrete subclass for AEF Holdings worksheet."""

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 4 Holdings"

		self.field_reg_exp_tuples	=	[
											["Cooperative approach ID", "CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Authorization ID", "[A-Za-z0-9 \-]+", "' can only contain alphanumeric, space, and hyphen characters."],
											["First transferring participating Party ID", "[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Party ITMO registry ID", "[A-Z]{3}\d{2}", "' must be a Party ID followed by two digits"],
											["First ID", "", ""],
											["Last ID", "", ""],
											["", "", ""],
											["Underlying unit registry ID", "", ""],
											["First unit ID", "", ""],
											["Last unit ID", "", ""],
											["", "", ""],
											["Metric", "GHG|non\-GHG", "' must 'GHG' or 'non-GHG'"],
											["Applicable GWP value(s)", "", ""],
											["Applicable non-GHG metric", "", ""],
											["Quantity (t CO2 eq)", "blankable|NA|\d+", "' must be a numerical value."],
											["Quantity (in non-GHG metric)", "blankable|NA|\d+", "' must be a numerical value."],
											["", "", ""],
											["Mitigation type", "", ""],
											["Vintage", "d{4}", "' must be a year."]
										]

		super().__init__(worksheet, field_names)


class AEFAuthEntities(RowFieldsSheet):
	"""Concrete subclass for AEF Authorized Entities worksheet."""

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 5 Auth. entities"

		self.field_reg_exp_tuples	=	[
											["Date of the authorization", "blankable|dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Name", "", ""],
											["Country of incorporation", "blankable|[A-Z][A-Za-z \(\)\']+", "'' is not a recognised Party Name."],	# Capitalised alphabet string contains spaces, brackets, apostrophes],
											["Identification number", "", ""],
											["Cooperative approach ID", "blankable|CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Conditions", ""],
											["Change and revocation conditions", "", ""],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)


class ColumnFieldsSheet(AEFSheet):
	"""Abstract superclass for checking worksheets with fields organised in columns."""


	def check_field_names(self, str_results):
		heading_row			= 0
		fields_start_row	= 0
		fields_end_row		= 0
		fields_column		= 0
		template_fields		= self.field_names
		n_template_fields	= len(template_fields)
		worksheet			= self.worksheet
		for row in worksheet.iter_cols(min_row=worksheet.min_row, max_row=worksheet.max_row, min_col=worksheet.min_column, max_col=worksheet.max_column):
			for cell in row:
				if ((cell.data_type == "s") and (cell.value.casefold() == template_fields[0].casefold())):
					heading_row	= cell.row
					fields_column	= cell.column
					continue
				elif ((heading_row > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[1].casefold())):
					fields_start_row	= cell.row
					continue
				elif ((fields_start_row > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[n_template_fields - 1].casefold())):
					fields_end_row	= cell.row
					break
		if (heading_row == 0):
			str_results[0]	+= "\n\t\tCould not find '" + template_fields[0] + "' section in '" + worksheet.title + "' worksheet."
			return False
		elif (fields_start_row == 0):
			str_results[0]	+= "\n\t\tCould not find '" + template_fields[1] + "' field in '" + worksheet.title + "' worksheet."
			return False
		elif (fields_end_row == 0):
			str_results[0]	+= "\n\t\tCould not find '" + template_fields[n_template_fields - 1] + "' field in '" + worksheet.title + "' worksheet."
			return False
		elif ((fields_end_row - fields_start_row + 1) != n_template_fields - 1):
			str_results[0]	+= "\n\t\tNumber of fields for the '" + template_fields[0] + "' in '" + worksheet.title + "' worksheet is incorrect."
			return False

		dest_fields	= []
		for row in worksheet.iter_cols(min_col=fields_column, max_col=fields_column, min_row=fields_start_row, max_row=fields_end_row, values_only=True):
			dest_fields.append(row)

		for x_field in range (1, n_template_fields):
			if (template_fields[x_field] in dest_fields[0]) is False:
				str_results[0]	+= "\n\t\tThe field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + "' of the Summary worksheet."
				return False
		return True


class AEFSummary(ColumnFieldsSheet):

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
		sheet_report	= AEFSheetReport(self.template_sheet_name)
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
			cell_report	= AEFCellReport(None, "Could not find worksheet '" + self.template_sheet_name + "'.")
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


class AEFSubmission(ColumnFieldsSheet):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 1 Submission"

		self.field_reg_exp_tuples	=	[
											["Party", "[A-Z][A-Za-z \(\)\']+", "'' is not a recognised Party Name."],	# Capitalised alphabet string contains spaces, brackets, apostrophes
											["Version", "[0-9]+\.[0-9]+", "' must conform to X.Y."],
											["Reported year", "\d{4}", "'' must be a four digit year."],
											["Date of submission", "dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Review status of the initial report", "\{Information in this field is populated by the CARP\}", "' must not be changed.  It is for secretariat use."],
											["Result of the consistency check of this AEF submission", "\{Information in this field is populated by the CARP\}", "'' must not be changed.  It is for secretariat use."],
											["First year of the NDC implementation period", "\d{4}", "'' must be a four digit year."],
											["Last year of the NDC implementation period", "\d{4}", "'' must be a four digit year."],
											["Reference to the Article 6 technical expert review report of the initial report", "\{Link to be produced by the CARP\}", "'' must not be changed.  It is for secretariat use."]
										]
		super().__init__(worksheet, field_names)


	def check_content(self, check_report):

		sheet_report	= AEFSheetReport("Checking the content of '" + self.template_sheet_name + "'")
		check_report.add_sheet_report(sheet_report)

		fields_start_row	= 0
		fields_end_row		= 0
		fields_column		= 0
		template_fields		= self.field_names
		n_template_fields	= len(template_fields)
		worksheet			= self.worksheet
		for row in worksheet.iter_cols(min_row=worksheet.min_row, max_row=worksheet.max_row, min_col=worksheet.min_column, max_col=worksheet.max_column):
			for cell in row:
				if ((cell.data_type == "s") and (cell.value.casefold() == template_fields[1].casefold())):
					fields_start_row	= cell.row
					fields_column		= cell.column
					continue
				elif ((fields_start_row > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[n_template_fields - 1].casefold())):
					fields_end_row	= cell.row
					break

		column		= fields_column + 1	# content is in the column after the field names
		x_tuple		= 0
		is_valid	= True
		for x_row in range(fields_start_row, fields_end_row):
			if (self.check_cell_content(x_row, column, x_tuple, sheet_report)) is False:
				is_valid	= False
			x_tuple	+= 1
		return is_valid


	def check_cell_content(self, x_target_row, x_target_column, x_tuple, sheet_report):
		field_reg_exp_tuple	= self.field_reg_exp_tuples[x_tuple]
		field_name			= field_reg_exp_tuple[0]
		field_reg_exp		= field_reg_exp_tuple[1]
		field_error_mesg	= field_reg_exp_tuple[2]
		cell	= self.worksheet.cell(x_target_row, x_target_column)
		if (cell.data_type == 'd'):
			if (re.match(field_reg_exp, str(cell.number_format)) == None):
				str_message	= "Cell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy"
				self.add_comment(cell, str_message)
				# str_link	= "#" + self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
				str_link	= self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
				cell_report	= AEFCellReport(str_link, str_message)
				sheet_report.add_cell_report(cell_report)
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:
			str_message	= "Cell content error: The value provided for '" + field_name + field_error_mesg
			self.add_comment(cell, str_message)
			# str_link	= "#" + self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
			str_link	= self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
			cell_report	= AEFCellReport(str_link, str_message)
			sheet_report.add_cell_report(cell_report)
			return False
		return True
