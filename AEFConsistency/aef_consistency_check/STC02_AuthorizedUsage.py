#STC02_AuthorizedUsage.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class STC02_AuthorizedUsage(AEFConsistencyCheck):
    """ Verify the authorization of an ITMO is consistent with the actual usage.
    """


    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("STC02: Authorization of ITMOs is consistent with actual usage.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        is_valid    = True
        submission  = self.submission
        actions     = submission.actions
        cursor      = self.cursor

        for action in actions:
            if (action.action_type in ["Cancellation", "First Transfer", "Use"]):
                auth_id = action.authorization_id
                ca_id   = action.cooperative_approach_id
                purpose = action.purpose
                cursor.execute(f'SELECT cooperative_approach_id  FROM {self.authorizations_table_name} WHERE authorization_id = ? AND purposes_for_auth = ?', (auth_id, purpose))
                db_rows = cursor.fetchall()
                if (len(db_rows) == 0):
                    cursor.execute(f'SELECT purposes_for_auth  FROM {self.authorizations_table_name} WHERE authorization_id = ?', (auth_id, ))
                    db_row      = cursor.fetchone()
                    db_purpose  = db_row[0] if (db_row is not None) else "N/A"
                    self.check_report.add_error_report("Authorization id: '" + auth_id + "' with purpose: '" + db_purpose + "' not consistent with action on " + str(action.action_date)+ "' with purpose: '" + purpose)
                    is_valid    = False
        return is_valid
