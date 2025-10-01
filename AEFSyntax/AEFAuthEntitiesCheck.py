# AEFAuthEntitiesCheck.py
#
# Checks the content of the Auth. entities worksheet
#

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck

class AEFAuthEntitiesCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 5 Auth. entities"

		self.field_reg_exp_tuples	=	[
											["Date of the authorization", "blankable|dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Name", "", ""],
											["Country of incorporation", "blankable|[A-Z][A-Za-z \(\)\']+", "'' is not a recognised Party Name."],	# Capitalised alphabet string contains spaces, brackets, apostrophes],
											["Identification number", "", ""],
											["Cooperative approach ID", "blankable|CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Conditions", ""],
											["Change and revocation conditions", "", ""],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)
