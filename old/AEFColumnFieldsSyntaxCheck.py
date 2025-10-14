# AEFColumnFieldsSyntaxCheck.py
#
# Check for worksheet whose fields are arranged in a column

from AEFSheetSyntaxCheck import AEFSheetSyntaxCheck


class AEFColumnFieldsSyntaxCheck(AEFSheetSyntaxCheck):


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

