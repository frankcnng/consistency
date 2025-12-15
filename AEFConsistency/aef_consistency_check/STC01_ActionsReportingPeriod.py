#STC01_ActionsReportingPeriod.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class STC01_ActionsReportingPeriod(AEFConsistencyCheck):
    """ Verify the reported actions correspond to the reporting period.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("STC01: Actions correspond to reporting period.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        is_valid        = True
        submission      = self.submission
        reported_year   = submission.reported_year
        actions         = submission.actions

        for action in actions:
            action_date = action.action_date
            action_year = int(action_date[0:4])
            if (action_year != reported_year):
                str_error   = "Action date: " + str(action_year) + " inconsistent with reported year: " + str(reported_year)
                self.check_report.add_error_report(str_error)
                is_valid    = False
        return is_valid
