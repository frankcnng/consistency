# AEFActionsCheck.py

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFActionsCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 3 Actions"
		super().__init__(worksheet, field_names)
