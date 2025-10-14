# AEFRowFieldsSyntaxCheck.py
#
# Check for worksheet whose fields are arranged in rows
#

import re

from AEFSheetSyntaxCheck import AEFSheetSyntaxCheck

import syntaxreport


class AEFRowFieldsSyntaxCheck(AEFSheetSyntaxCheck):

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
			cell_report	= syntaxreport.AEFCheckCellReport(str_link, "Could not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet."
			return False
		elif (fields_start_column == 0):
			cell_report	= syntaxreport.AEFCheckCellReport(str_link, "Could not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet."
			return False
		elif (fields_end_column == 0):
			cell_report	= syntaxreport.AEFCheckCellReport(str_link, "Could not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tCould not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] +"' worksheet."
			return False
		elif ((fields_end_column - fields_start_column - n_blank_cells + 1) != (n_template_fields - 1)):	# (n_template_fields - 1) as the first element of array is sheet name
			cell_report	= syntaxreport.AEFCheckCellReport(str_link, "Could not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			sheet_report.add_cell_report(cell_report)
#			str_results[0]	+= "\n\t\tNumber of fields in '" + template_fields[0] + "' worksheet is incorrect."
			return False

		dest_fields	= []
		for column in worksheet.iter_rows(min_col=fields_start_column, max_col=fields_end_column, min_row=field_headings_row, max_row=field_headings_row, values_only=True):
			dest_fields.append(column)

		for x_field in range (1, n_template_fields):
			if (template_fields[x_field] in dest_fields[0]) is False:
				cell_report	= syntaxreport.AEFCheckCellReport(str_link, "The field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet.")
				sheet_report.add_cell_report(cell_report)
#				str_results[0]	+= "\n\t\tThe field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet."
				return False
		return True


	def check_content(self, sheet_report):
	# Check the contents of the fields in the sheet are syntactically correct
	#
		cell_report	= syntaxreport.AEFCheckCellReport(None, "Checking the content of '" + self.template_sheet_name + "'")
		sheet_report.add_cell_report(cell_report)
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
