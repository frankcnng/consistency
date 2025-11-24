# main.py
#
# Checks the syntax of AEF files
#

# Load os and shell libraries
import os, shutil

# Load the openpyxl Excel library
from openpyxl import load_workbook

from aef_structure_check import AEFStructureCheck
from aef_content_check import AEFContentCheck
from syntaxreport.AEFBookReport import AEFBookReport


# The directory containing AEF files to be checked
aef_dir			= "/Users/frankng/United Nations Framework Convention on Climate Change/Mitigation - Article 6.2/03_CARP/consistency/AEF_files/"
unprocessed_dir	= aef_dir + "00.unprocessed/"
archive_dir		= aef_dir + "99.archive/"
passed_dir		= aef_dir + "10.syntax.passed/"
failed_dir		= aef_dir + "11.syntax.failed/"
#aef_dir		= "../AEF_files.00.unchecked/"


def main():
	"""Check all .xlsx files in aef_dir for valid AEF syntax.
	Files ending with '.syntax_checked.xlsx' are the output of this tool, and will be overwritten."""

	files	= os.listdir(unprocessed_dir)
	for str_file in files:
		if (str_file.endswith(".xlsx")):
			if str_file.endswith(".syntax_checked.xlsx"):
				continue
			else:
				str_head	= str_file[:-5]
				str_checked	= str_head + ".syntax_checked.xlsx"
				dst_path	= unprocessed_dir + str_checked
				src_path	= unprocessed_dir + str_file
				shutil.copyfile(src_path, dst_path)

				print ("\nChecking '" + str_file + "'")
				if (check_file(dst_path, str_file)):
					shutil.move(dst_path, passed_dir + str_checked)
				else:
					shutil.move(dst_path, failed_dir + str_checked)
				shutil.move(src_path, archive_dir + str_file)


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
	return check_report.is_valid


if __name__ == "__main__":
	main()
