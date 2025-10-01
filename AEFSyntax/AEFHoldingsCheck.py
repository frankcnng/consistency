# AEFHoldingsCheck.py

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFHoldingsCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 4 Holdings"
		super().__init__(worksheet, field_names)
