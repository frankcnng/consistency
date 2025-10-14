# AEFCellReport.py


class AEFCellReport:

	def __init__(self, cell_ref, str_mesg):
		self.cell_ref	= cell_ref
		self.str_mesg   = str_mesg


	def print(self, workbook, results_sheet, x_row):
		if (self.cell_ref != None):
			cell			= results_sheet.cell(x_row, 3)
			cell.hyperlink	= self.cell_ref
			cell.value		= "Link"
		results_sheet.cell(x_row, 4, value=self.str_mesg)
