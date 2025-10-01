# AEFHoldingsCheck.py

from AEFRowFieldsSyntaxCheck import AEFRowFieldsSyntaxCheck


class AEFHoldingsCheck(AEFRowFieldsSyntaxCheck):

	def __init__(self, worksheet, field_names):
		self.template_sheet_name	= "Table 4 Holdings"

		self.field_reg_exp_tuples	=	[
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
											["Quantity (t CO2 eq)", "blankable|NA|\d+", "' must be a numerical value."],
											["Quantity (in non-GHG metric)", "blankable|NA|\d+", "' must be a numerical value."],
											["", "", ""],
											["Mitigation type", "", ""],
											["Vintage", "d{4}", "' must be a year."]
										]

		super().__init__(worksheet, field_names)
