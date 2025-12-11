#II04_Metrics.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II04_Metrics(AEFConsistencyCheck):
    """ Verify that the metrics used for ITMOs are consistent
        across all relevant reports, tables and participating Parties.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II04: Verify that metrics used for ITMOs are consistent.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
            For each ITMO block in the submission, validate the metric is the same for all overlapping ITMO blocks in other submissions
        """
        cursor              = self.cursor
        action_table_name   = "Actions"
        holdings_table_name = "Holdings"
        itmo_tuples = self.get_itmo_tuples()

        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric, reporting_party_Id, reported_year, major_version, minor_version FROM {action_table_name}')
        db_rows = cursor.fetchall()
        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric, reporting_party_Id, reported_year, major_version, minor_version FROM {holdings_table_name}')
        db_rows.extend(cursor.fetchall())
        is_valid    = True
        for itmo_tuple in itmo_tuples:  # for each ITMO block in submission
            block, ca_id, metric   = itmo_tuple[0], itmo_tuple[1], itmo_tuple[2]
            
            # This block of code compares the metrics for each overlapping itmo block in all submissions
            for db_row in db_rows:      # for each row from db's actions and holdings tables
                db_ca_id, db_first_id, db_last_id, db_metric    = db_row[0], db_row[1], db_row[2], db_row[3]
                try:
                    itmo_block  = aef_submission.ITMOBlock(db_first_id, db_last_id)    # get the ITMO block from the db row
                except aef_submission.InvalidITMOBlockException as e:
                    self.check_report.add_error_report(str(e))
                    is_valid    = False
                else:
                    if (block.is_overlapping(itmo_block)):  # if the block from the db the overlapping (some ITMOs are the same) as the block from the submission
                        if (metric != db_metric):    # if the metric is not the same
                            self.check_report.add_error_report("ITMO with inconsistent metrics: '" + itmo_tuple[3] + "' - '" + itmo_tuple[4] + "' , metric: '" + metric + "'")
                            self.check_report.add_error_report("\tSubmission: " + db_row[4] + " " + str(db_row[5]) + " version " + str(db_row[6]) + "." + str(db_row[7]) + ", metric: '" + db_metric + "'")
                            is_valid    = False

            authorizations_table_name   = "Authorizations"
            db_ca_ids  = [] # list of all cooperative approach ids
            cursor.execute(f'SELECT metric, reporting_party_Id, reported_year, major_version, minor_version FROM {authorizations_table_name} WHERE cooperative_approach_id = ?', (ca_id, ))
            db_auth_rows    = cursor.fetchall()
            for db_auth_row in db_auth_rows:      # for each row from db's authorizations table with match cooperative approach id
                db_metric, db_reporting_party_Id, db_reported_year, db_major_version, db_minor_version    = db_auth_row[0], db_auth_row[1], db_auth_row[2], db_auth_row[3], db_auth_row[4]
                if (metric != db_metric):
                    self.check_report.add_error_report("ITMO with inconsistent metrics: '" + itmo_tuple[3] + "' - '" + itmo_tuple[4] + "' , metric: '" + metric + "'")
                    self.check_report.add_error_report("\tSubmission: " + db_reporting_party_Id + " " + str(db_reported_year) + " version " + str(db_major_version) + "." + str(db_minor_version) + ": cooperative approach id: " + ca_id + ", metric: '" + db_metric + "'")
                    is_valid    = False
        return is_valid
