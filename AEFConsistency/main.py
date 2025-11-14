# main.py
#
# Checks the consistency of AEF files
#

# Load os and shell libraries
import os, shutil

# Load the openpyxl Excel library
from openpyxl import load_workbook

from AEFStructureCheck import AEFStructureCheck
from AEFContentCheck import AEFContentCheck
from syntaxreport.AEFBookReport import AEFBookReport


# The directory containing AEF files to be checked
aef_dir				= "/Users/frankng/United Nations Framework Convention on Climate Change/Mitigation - Article 6.2/03_CARP/consistency/AEF_files/"
syntax_passed_dir	= aef_dir + "10.syntax.passed/"
consistent_dir		= aef_dir + "20.consistent/"
undetermined_dir	= aef_dir + "21.undetermined/"
inconsistent_dir	= aef_dir + "10.inconsistent/"



def main():
	"""Check all .xlsx files in aef_dir/syntax_passed_dir for AEF consistency.
	Files ending with '.consistency_checked.xlsx' are the output of this tool, and will be overwritten."""

	files	= os.listdir(syntax_passed_dir)
	for str_file in files:
		if (str_file.endswith(".xlsx")):
			if str_file.endswith(".consistency_checked.xlsx"):
				continue
			else:
				str_head	= str_file[:-5]
				dst_path	= aef_dir + str_head + ".consistency_checked.xlsx"
				src_path	= aef_dir + str_file
				shutil.copyfile(src_path, dst_path)

				print ("\nChecking '" + str_file + "'")
				check_file(dst_path, str_file)


def	load_file(str_path, str_file):
	""""Load the file with pathname 'str_path' into the database.
	The file has been syntax checked, so fields can be loaded into objects without checking.
	The local name of the file is 'str_file'."""

	load_workbook	= load_workbook(str_path)
	







def check_file(str_path, str_file):
	""""Check the file with pathname 'str_path'.
	The local name of the file is 'str_file'
	First the structure of the workbook is checked,
	next, the content of the fields in each sheet are checked."""

	workbook		= load_workbook(str_path)
	worksheets		= []
	field_names		= []
	check_report	= AEFBookReport(str_file)

	structureCheck = AEFStructureCheck()
	if structureCheck.check(workbook, worksheets, field_names, check_report) is False:
		check_report.is_valid = False
	else:
		contentCheck 			= AEFContentCheck()
		check_report.is_valid	= contentCheck.check(worksheets, field_names, check_report)
	check_report.print(workbook)
	
	workbook.save(str_path)


if __name__ == "__main__":
	main()
