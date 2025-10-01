# AEFSheetSyntaxCheck.py


class AEFSheetSyntaxCheck:

	def __init__(self, worksheet, field_names):
		self.worksheet		= worksheet
		self.field_names	= field_names


	def check_structure(self):
		print ("Checking the structure of '" + self.template_sheet_name + "'")
		return self.check_field_names()


	def check_content(self):

		return True