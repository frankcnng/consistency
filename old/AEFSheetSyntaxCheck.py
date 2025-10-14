# AEFSheetSyntaxCheck.py

from openpyxl.comments import Comment
import re

import syntaxreport


class AEFSheetSyntaxCheck:

	def __init__(self, worksheet, field_names):
		self.worksheet		= worksheet
		self.field_names	= field_names


	def check_structure(self, check_report):
		sheet_report	= syntaxreport.AEFCheckSheetReport(self.template_sheet_name)
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
				str_link	= "#" + self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
				cell_report	= syntaxreport.AEFCheckCellReport(str_link, str_message)
#				str_results[0]	+= "\n\t\tCell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy"
				return False
		elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:
			str_message	= "Cell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy"
			self.add_comment(cell, str_message)
			str_link	= "#" + self.template_sheet_name + "!" + self.coord2cell_ref(x_target_row, x_target_column)
			cell_report	= syntaxreport.AEFCheckCellReport(str_link, str_message)
#			str_results[0]	+= "\n\t\tCell content error: The value provided for '" + field_name + field_error_mesg
			return False
		return True


	def add_comment(self, cell, str_comment):
		comment	= Comment(str_comment)
		cell.comment	= comment


	def coord2cell_ref(x_row, x_column):
		# return the alpha number excel cell reference from row number and column number (1-based)
		if (x_column <= 26):
			return (chr(ord('A') + x_column - 1) + str(x_row))
		else:
			return ("A" + chr(ord('A') + (x_column % 26) - 1) + str(x_row))