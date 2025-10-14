# AEFCellReport.py

from openpyxl.styles import Font

class AEFCellReport:

	def __init__(self, cell_ref, str_mesg):
		self.cell_ref	= cell_ref
		self.str_mesg   = str_mesg


	def print(self, workbook, results_sheet, x_row):
		if (self.cell_ref != None):
			cell			= results_sheet.cell(x_row, 4)
			cell.font		= Font(color='0000FF', underline='single')
			cell.value		= "Link"
			cell.hyperlink	= self.cell_ref
		results_sheet.cell(x_row, 5, value=self.str_mesg)
