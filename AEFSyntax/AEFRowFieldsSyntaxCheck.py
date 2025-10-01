# AEFHoldings.py
#
# Check for worksheet whose fields are arranged in rows

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
							# print ("row is " + str(cell.row))
							# print ("col is " + str(cell.column))
							# print ("blanks is " + str(n_blank_cells))
							# print ()
							continue
						elif ((fields_start_column > 0) and (cell.data_type == "s") and (cell.value.casefold() == template_fields[n_template_fields - 1].casefold())):
							fields_end_column	= cell.column
							break
					else:
						break

		if (heading_column == 0):
			print ("Could not find '" + template_fields[0] + "' heading in the '" + template_fields[0] + "' worksheet.")
			return False
		elif (fields_start_column == 0):
			print ("Could not find '" + template_fields[1] + "' heading in the '" + template_fields[0] + "' worksheet.")
			return False
		elif (fields_end_column == 0):
			print ("Could not find '" + template_fields[n_template_fields - 1] + "' heading in the '" + template_fields[0] +"' worksheet.")
			return False
		elif ((fields_end_column - fields_start_column - n_blank_cells + 1) != (n_template_fields - 1)):	# (n_template_fields - 1) as the first element of array is sheet name
			# print ("template fields: " + str(n_template_fields - 1))
			# print ("start col: " + str(fields_start_column))
			# print ("end col: " + str(fields_end_column))
			# print ("blanks: " + str(n_blank_cells))
			# print ("fields in sheet: " + str(fields_end_column - fields_start_column - n_blank_cells + 1))
			print ("Number of fields in '" + template_fields[0] + "' worksheet is incorrect.")
			return False

		dest_fields	= []
		for column in worksheet.iter_rows(min_col=fields_start_column, max_col=fields_end_column, min_row=field_headings_row, max_row=field_headings_row, values_only=True):
			dest_fields.append(column)

		for x_field in range (1, n_template_fields):
			if (template_fields[x_field] in dest_fields[0]) is False:
				print ("The field '" + template_fields[x_field] + "' cannot be found in '" + template_fields[0] + " worksheet.")
				return False
		return True
