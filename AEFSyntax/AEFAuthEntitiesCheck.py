# AEFAuthEntitiesCheck.py

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFAuthEntitiesCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 5 Auth. entities"
		super().__init__(worksheet, field_names)
