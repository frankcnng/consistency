# AEFSheetReport.py

from openpyxl.comments import Comment

from syntaxreport.AEFCellReport import AEFCellReport


class AEFSheetReport:

	def __init__(self, str_title, x_indent):
		self.str_title      = str_title
		self.x_indent		= x_indent
		self.cell_reports   = []


	def add_cell_report(self, str_sheet_name, cell, str_message):
		self.add_comment(cell, str_message)
		str_link	= "#'" + str_sheet_name + "'" + "!" + self.coord2cell_ref(cell.row, cell.column)
		cell_report	= AEFCellReport(str_link, str_message)
		self.cell_reports.append(cell_report)


	def add_comment(self, cell, str_comment):
		comment	= Comment(str_comment, "AEFSyntaxCheck")
		cell.comment	= comment


	def coord2cell_ref(self, x_row, x_column):
		# return the alpha number excel cell reference from row number and column number (1-based)
		if (x_column <= 26):
			return (chr(ord('A') + x_column - 1) + str(x_row))
		else:
			return ("A" + chr(ord('A') + (x_column % 26) - 1) + str(x_row))


	def print(self, workbook, results_sheet, x_row):
		results_sheet.cell(x_row, self.x_indent, value=self.str_title)
		x_row	+= 1
		for cell_report in self.cell_reports:
			cell_report.print(workbook, results_sheet, x_row)
			x_row   += 1
		return (x_row)