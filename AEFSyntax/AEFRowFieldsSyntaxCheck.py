# AEFHoldings.py
#
# Check for worksheet whose fields are arranged in rows
#

import re

from AEFSheetSyntaxCheck import AEFSheetSyntaxCheck


class AEFRowFieldsSyntaxCheck(AEFSheetSyntaxCheck):

	def check_field_names(self):
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

		if (heading_column == 0):
			print ("\tCould not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			return False
		elif (fields_start_column == 0):
			print ("\tCould not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			return False
		elif (fields_end_column == 0):
			print ("\tCould not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] +"' worksheet.")
			return False
		elif ((fields_end_column - fields_start_column - n_blank_cells + 1) != (n_template_fields - 1)):	# (n_template_fields - 1) as the first element of array is sheet name
			print ("\tNumber of fields in '" + template_fields[0] + "' worksheet is incorrect.")
			return False

		dest_fields	= []
		for column in worksheet.iter_rows(min_col=fields_start_column, max_col=fields_end_column, min_row=field_headings_row, max_row=field_headings_row, values_only=True):
			dest_fields.append(column)

		for x_field in range (1, n_template_fields):
			if (template_fields[x_field] in dest_fields[0]) is False:
				print ("The field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet.")
				return False
		return True


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


	# def check_cell_content(self, x_target_row, x_target_column, x_tuple):
	# 	field_reg_exp_tuple	= self.field_reg_exp_tuples[x_tuple]
	# 	field_name			= field_reg_exp_tuple[0]
	# 	field_reg_exp		= field_reg_exp_tuple[1]

	# 	if (field_reg_exp == ""):
	# 		return True

	# 	field_error_mesg	= field_reg_exp_tuple[2]
	# 	cell				= self.worksheet.cell(x_target_row, x_target_column)
	# 	if (re.match("^blankable", field_reg_exp) != None):	# if the cell can be either blank, of a defined set of values
	# 		if (cell.value == None):	# if the cell is empty
	# 			return True

	# 	if (cell.data_type == 'd'):
	# 		if (re.match(field_reg_exp, str(cell.number_format)) == None):
	# 			print ("\tCell content error: The value provided for '" + field_name + " must be in the format dd/mm/yyyy")
	# 			return False
	# 	elif (re.fullmatch(field_reg_exp, str(cell.value))) == None:

	# 		print ("\tCell content error: The value provided for '" + field_name + field_error_mesg)
	# 		return False
	# 	return True


