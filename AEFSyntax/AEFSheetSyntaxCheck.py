# AEFSheetSyntaxCheck.py

import re


class AEFSheetSyntaxCheck:

	def __init__(self, worksheet, field_names):
		self.worksheet		= worksheet
		self.field_names	= field_names


	def check_structure(self, str_results):
		str_results[0]	+= "\n\tChecking the structure of '" + self.template_sheet_name + "'"
		return self.check_field_names(str_results)


	def check_field_names(self, str_results):
		return True


	def check_content(self, str_results):
		return True
	

	def check_cell_content(self, x_target_row, x_target_column, x_tuple, str_results):
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
				str_results[0]	+= "\n\t\tCell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy"
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:

			str_results[0]	+= "\n\t\tCell content error: The value provided for '" + field_name + field_error_mesg
			return False
		return True
