#II03_SectorsActivityTypes.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II03_SectorsActivityTypes(AEFConsistencyCheck):
    """ Verify that the sectors and activity types for each ITMO remain consistent
        throughout their lifecycle and across all relevant reports, tables, and participating Parties.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II03: Verify that sectors and activity types for each ITMO remain consistent.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        cursor              = self.cursor
        action_table_name   = "Actions"
        holdings_table_name = "Holdings"
        itmo_tuples         = self.get_itmo_tuples()

        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric FROM {action_table_name}')
        db_rows = cursor.fetchall()
        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric FROM {holdings_table_name}')
        db_rows.extend(cursor.fetchall())

        authorizations_table_name   = "Authorizations"
        is_valid                    = True
        for itmo_tuple in itmo_tuples:  # for each ITMO block in submission
            block, ca_id, metric   = itmo_tuple[0], itmo_tuple[1], itmo_tuple[2]
            
            cursor.execute(f'SELECT sectors, activity_types FROM {authorizations_table_name} WHERE cooperative_approach_id = ?', (ca_id, ))
            db_auth_rows    = cursor.fetchall()
            set_sectors, set_activity_types     = set(), set()
            for db_auth_row in db_auth_rows:    # for each authorization in the db with cooperative approach id of ca_id
                db_sectors, db_activity_types   = db_auth_row[0], db_auth_row[1]
                str_sectors                     = self.normalise_str_names(db_sectors)
                str_activity_types              = self.normalise_str_names(db_activity_types)
                set_sectors.add(str_sectors)
                set_activity_types.add(str_activity_types)

            if (len(set_sectors) > 1):
                str_error   = "ITMO with inconsistent sectors: '" + itmo_tuple[3] + "' - '" + itmo_tuple[4] + "' with cooperative approach id: '" + ca_id + "' : " + str(set_sectors)
                self.check_report.add_error_report(str_error)
                is_valid    = False
            if (len(set_activity_types) > 1):
                str_error   = "ITMO with inconsistent activity types: '" + itmo_tuple[3] + "' - '" + itmo_tuple[4] + "' with cooperative approach id: '" + ca_id + "' : " + str(set_activity_types)
                self.check_report.add_error_report(str_error)
                is_valid    = False

        return is_valid
