# AEFActionsCheck.py
#
# Checks the content of the Actions worksheet
#

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFActionsCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 3 Actions"

		self.field_reg_exp_tuples	=	[
											["Action date", "dd/mm/yyyy", "'' must be in the format: dd/mm/yyyy"],
											["Action type", "Acquistion|Transfer|Use|Cancellation|First transfer", "'' must be one of 'Acquistion', 'Transfer', 'Use', 'Cancellation', 'First transfer'"],
											["Action subtype", "", ""],
											["Cooperative approach ID", "CA\d{4}", "' must start with 'CA' followed by four digits."],
											["Authorization ID", "[A-Za-z0-9 \-]+", "' can only contain alphanumeric, space, and hyphen characters."],
											["First transferring participating Party ID", "[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Party ITMO registry ID", "[A-Z]{3}\d{2}", "' must be a Party ID followed by two digits"],
											["First ID", "", ""],
											["Last ID", "", ""],
											["", "", ""],
											["Underlying unit registry ID", "", ""],
											["First unit ID", "", ""],
											["Last unit ID", "", ""],
											["", "", ""],
											["Metric", "GHG|non\-GHG", "' must 'GHG' or 'non-GHG'"],
											["Applicable GWP value(s)", "", ""],
											["Applicable non-GHG metric", "", ""],
											["Quantity (t CO2 eq)", "blankable|\d+", "' must be a numerical value."],
											["Quantity (in non-GHG metric)", "blankable|\d*", "' must be a numerical value."],
											["", "", ""],
											["Mitigation type", "", ""],
											["Vintage", "blankable|\d{4}", "' must be a year."],
											["", "", ""],
											["Transferring participating Party ID", "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Acquiring participating Party ID",  "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["", "", ""],
											["Purpose for which the ITMO has been used towards or cancelled for OIMP", "", ""],
											["Using/cancelling participating Party ID", "blankable|[A-Z]{3}", "' must an ISO 3166 alpha-3 country code."],
											["Using/cancelling authorized entity ID", "", ""],
											["Calendar year for which the ITMOs are used towards the Party's NDC", "blankable|\d{4}", "' must be a year."],
											["", "", ""],
											["Result of the consistency checks", "", ""],
											["Additional explanatory information", "", ""]
										]

		super().__init__(worksheet, field_names)
