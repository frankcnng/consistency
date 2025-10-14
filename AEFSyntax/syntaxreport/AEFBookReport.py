# AEFBookReport.py

# Load the openpyxl Excel library
from openpyxl import load_workbook


class AEFBookReport:

	def __init__(self, str_title):
		self.str_title      = str_title
		self.sheet_reports  = []
		self.str_success    = "Syntax check completed successfully."
		self.str_fail       = "Syntax check found errors."
		self.is_valid       = True

	def add_sheet_report(self, sheet_report):
		self.sheet_reports.append(sheet_report)
		return True


	# def is_valid(self, is_valid):
	# 	self.is_valid   = is_valid


	def print(self, workbook):
		results_sheet	= workbook.create_sheet(title = "Syntax check results", index = 7)
		x_row			= 1
		x_column		= 1

		results_sheet.cell(x_row, x_column, value=self.str_title)
		x_row	+= 1

		for sheet_report in self.sheet_reports:
			x_row	= sheet_report.print(workbook, results_sheet, x_row)
		x_row	+= 1

		if (self.is_valid):
			str_result  = self.str_success
		else:
			str_result  = self.str_fail
		results_sheet.cell(x_row, 1, value=str_result)

	