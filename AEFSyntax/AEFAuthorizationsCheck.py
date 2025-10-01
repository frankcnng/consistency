# AEFAuthorizationsCheck.py
#
# Checks the content of the Authorizations worksheet
#

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFAuthorizationsCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 2 Authorizations"

		self.field_reg_exp_tuples	=	[
											["Authorization ID", "[A-Za-z0-9 \-]+", "' can only contain alphanumeric, space, and hyphen characters."],
											["Date of authorization", "dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Cooperative approach ID", "CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Version of the authorization", "\d+", "' must be a number."],
											["", "", ""],
											["Authorized quantity", "\d+", "' must be a number."],
											["Metric", "GHG|non\-GHG", "' must 'GHG' or 'non-GHG'"],
											["Applicable GWP value(s)", "", ""],
											["Applicable non-GHG metric", "", ""],
											["Sector(s)", "[A-Za-z0-9 ]+", "' can only contain alphanumeric, and space characters."],
											["Activity type(s)", "[A-Za-z0-9 ]+", "' can only contain alphanumeric, and space characters."],
											["Purposes for authorization", "NDC|OIMP|IMP|OP|NDC and OIMP|NDC and IMP|NDC and OP", "' must be one of 'NDC', 'OIMP', 'IMP', 'OP', 'NDC and OIMP', 'NDC and IMP', or 'NDC and OP'."],
											["Authorized Party(ies) ID", "[A-Z]{3}( *, *[A-Z]{3})*", "' must a comma-separated list of ISO 3166 alpha-3 codes."],
											["Authorized entity(ies) ID", "[A-Za-z0-9 \-]+( *, *[A-Za-z0-9 \-]+)*", "' must a comma-separated list of entity names."],
											["OIMP authorized by the Party", "", ""],
											["Authorized timeframe", "blankable|(\d{4} *\- *\d{4})*", "' must be empty of a year range (dddd - dddd)"],
											["Authorization terms and conditions", "", ""],
											["Authorization documentation", "", ""],
											["First transfer definition for OIMP", "blankable|Authorization|Issuance|Use of cancellation", "' must be empty or one of 'Authorization', 'Issuance', 'Use of cancellation;."],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)
