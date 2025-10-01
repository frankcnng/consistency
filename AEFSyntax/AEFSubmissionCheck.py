# AEFSubmissionCheck.py
#
# Check the Submission worksheet
#

import re

from AEFColumnFieldsSyntaxCheck import AEFColumnFieldsSyntaxCheck


class AEFSubmissionCheck(AEFColumnFieldsSyntaxCheck):

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


	def check_content(self):

		print ("\nChecking the content of '" + self.template_sheet_name + "'")

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
			if (self.check_cell_content(x_row, column, x_tuple)) is False:
				is_valid	= False
			x_tuple	+= 1
		return is_valid


	def check_cell_content(self, x_target_row, x_target_column, x_tuple):
		field_reg_exp_tuple	= self.field_reg_exp_tuples[x_tuple]
		field_name			= field_reg_exp_tuple[0]
		field_reg_exp		= field_reg_exp_tuple[1]
		field_error_mesg	= field_reg_exp_tuple[2]
		cell	= self.worksheet.cell(x_target_row, x_target_column)
		if (cell.data_type == 'd'):
			if (re.match(field_reg_exp, str(cell.number_format)) == None):
				print ("	Cell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy")
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:
			print ("	Cell content error: The value provided for '" + field_name + field_error_mesg)
			return False
		return True



