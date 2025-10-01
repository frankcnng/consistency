# Load os library
import os

# Load the openpyxl Excel library
from openpyxl import load_workbook

from AEFStructure import AEFStructure
from AEFContent import AEFContent


# The directory containing AEF files to be checked
#aef_dir	= "/Users/frankng/United Nations Framework Convention on Climate Change/Mitigation - Article 6.2/03_CARP/consistency/AEF_files/"
aef_dir	= "../AEF_files/"


def main():
	files	= os.listdir(aef_dir)
	for file in files:
		if check_file(file):
			print("'" + file + "' is a valid AEF file.")
		else:
			print("'" + file + "' contains errors")


def check_file(file):
	print("\nChecking '" + file + "'")
	workbook = load_workbook(aef_dir + "/" + file)
	worksheets	= []
	field_names	= []

	structure = AEFStructure()
	if structure.check(workbook, worksheets, field_names) is False:
		return False
	content = AEFContent()
	if content.check(worksheets, field_names) is False:
		return False
	return True


def check_content(workbook):
	return True


if __name__ == "__main__":
	main()
