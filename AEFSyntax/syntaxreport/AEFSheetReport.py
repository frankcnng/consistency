# AEFSheetReport.py


class AEFSheetReport:

	def __init__(self, str_title):
		self.str_title      =	str_title
		self.cell_reports   = []


	def add_cell_report(self, cell_report):
		self.cell_reports.append(cell_report)


	def print(self, workbook, results_sheet, x_row):
		x_column    = 2
		results_sheet.cell(x_row, x_column, value=self.str_title)
		x_row	+= 1
		for cell_report in self.cell_reports:
			cell_report.print(workbook, results_sheet, x_row)
			x_row   += 1
		return (x_row)
