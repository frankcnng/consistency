# main.py
#
# Checks the consistency of AEF files
#

# Load os and shell libraries
import os, shutil

# Load the openpyxl Excel library
from openpyxl import load_workbook
import sqlite3

import aef_sheet_check
from create_db import create_tables


# The directory containing AEF files to be checked
aef_dir				= "/Users/frankng/United Nations Framework Convention on Climate Change/Mitigation - Article 6.2/03_CARP/consistency/AEF_files/"
syntax_passed_dir	= aef_dir + "10.syntax.passed/"
consistent_dir		= aef_dir + "20.consistent/"
undetermined_dir	= aef_dir + "21.undetermined/"
inconsistent_dir	= aef_dir + "10.inconsistent/"


def main():
	"""Check all .xlsx files in aef_dir/syntax_passed_dir for AEF consistency.
	Files ending with '.consistency_checked.xlsx' are the output of this tool, and if any exist, will be overwritten."""

	conn	= create_tables(":memory:")	#create an in-memory database for consistency checking
	cursor	= conn.cursor()
	load_submissions(syntax_passed_dir, cursor)
	print_tables(cursor)
#	check_submissions(cursor)


def print_table(cursor, table_name):
	"""Print the contents of the specified table using the provided cursor.
	"""
	print(f'\n{table_name}:\n')
	cursor.execute(f'SELECT * FROM {table_name}')
	rows	= cursor.fetchall()
	for row in rows:    
		print(row)
	print("\n")
	return


def print_tables(cursor):
	"""Print the contents of all tables in the database using the provided cursor.
	"""
	tables	=	[
					"Submissions",
					"Authorizations",
					"Actions",
					"Holdings",
					"Authorized_Entities"
				]
	for table in tables:
		print_table(cursor, table)
	return


def	load_submissions(str_path, cursor):
	""""Load AEF submission files in pathname 'str_path' into the database.
	The files have been syntax checked, so fields can be loaded into objects without checking.
	"""

	files	= os.listdir(str_path)
	for str_file in files:
		if (str_file.endswith(".xlsx")):
			if str_file.endswith(".consistency_checked.xlsx"):	# ignore these files, they will be overwritten
				continue
			else:
				full_path	= str_path + str_file		# full pathname of source file
				str_head	= str_file[:-5]				# filename without '.xlsx' suffix

				str_checked	= str_head + ".consistency_checked.xlsx"	# filename of destination file
				dst_path	= str_path + str_checked					# full pathname of destination file
				src_path	= str_path + str_file						# full pathname of source file
				shutil.copyfile(src_path, dst_path)						# copy source to destination

				print ("Loading '" + str_file + "' into database...")
				workbook	= load_workbook(dst_path, data_only=True)
				load_workbook2db(workbook, cursor)
	return


def	load_workbook2db(workbook, cursor):
	""""Load all data sheets of workbook into the database.
	The workbook has been syntax checked, so fields can be loaded into objects without checking."""

	submission_check	= aef_sheet_check.AEFSubmissionCheck(workbook)
	submission_check.load_to_db(cursor)
	submission_key		= submission_check.primary_key	# the submission primary key is used as the foreign key from other tables

	authorizations_check	= aef_sheet_check.AEFAuthorizationsCheck(workbook)
	authorizations_check.load_to_db(cursor, submission_key)
	actions_check			= aef_sheet_check.AEFActionsCheck(workbook)
	actions_check.load_to_db(cursor, submission_key)
	holdings_check			= aef_sheet_check.AEFHoldings(workbook)
	holdings_check.load_to_db(cursor, submission_key)
	auth_entities_check		= aef_sheet_check.AEFAuthEntitiesCheck(workbook)
	auth_entities_check.load_to_db(cursor, submission_key)	
	return


def check_submissions(cursor):
	""""Check all submissions in the database for consistency.
	Update the consistency_status field in the Submissions table."""

	# Placeholder for consistency checking logic
	# For each submission, perform checks and update the consistency_status accordingly

	# Example update (to be replaced with actual logic)
	cursor.execute("""
	UPDATE Submissions
	SET consistency_status = 'Consistent'
	WHERE consistency_status IS NULL;
	""")
	return


if __name__ == "__main__":
	main()
