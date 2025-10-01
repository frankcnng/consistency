# AEFAuthorizationsCheck.py

import re

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFAuthorizationsCheck(AEFRowFieldsSyntaxCheck):

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


	def check_content(self):

		print ("\nChecking the content of '" + self.template_sheet_name + "'")

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
			if (self.check_cell_content(row, x_column, x_tuple)) is False:
				is_valid	= False
			x_tuple	+= 1
		return is_valid


	def check_cell_content(self, x_target_row, x_target_column, x_tuple):
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
				print ("	Cell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy")
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:

			print ("	Cell content error: The value provided for '" + field_name + field_error_mesg)
			return False
		return True


