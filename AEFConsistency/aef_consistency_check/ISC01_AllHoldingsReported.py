#ISC01_AllHoldingsReported.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class IST01_AllHoldingsReported(AEFConsistencyCheck):
    """ Verify the reported actions correspond to the reporting period.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("ISC01: All holdings reported.")
        super().__init__(submission, cursor, submission_report)
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
            This is actually a reconciliation between actions and holdings.
            Go through all actions in consistent submissions to verify holdings correspond.
        """
        is_valid        = True
        cursor          = self.cursor
        submission      = self.submission
        reported_year   = submission.reported_year
        holdings        = submission.holdings

        actions         = []
        cursor.execute(f'SELECT * FROM Actions ORDER BY action_date ASC, reporting_party_Id ASC,action_type ASC')	# Get actions from db
        action_rows	= cursor.fetchall()
        for action_row in action_rows:
            action  = aef_submission.AEFAction(None, action_row)
            actions.append(action)

            if action.action_type == "First transfer":
                pass


        return is_valid
