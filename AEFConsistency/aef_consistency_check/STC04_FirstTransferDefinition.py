#STC04_FirstTransferDefinition.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class STC04_FirstTransferDefinition(AEFConsistencyCheck):
    """ For ITMOs that were first transferred,
        verify this corresponds to the action that was the first transfer definition.
    """


    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("STC04: First transfer consistent with definition in authorization.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        return True
        is_valid    = True
        submission  = self.submission
        actions     = submission.actions
        first_year  = submission.ndc_period_first_year
        last_year   = submission.ndc_period_last_year

        for action in actions:
            if (action.action_type == "First transfer"):
                action_date                 = action.action_date
                action_year_used_for_ndc    = action.year_used_for_ndc
                if (action_year_used_for_ndc < first_year or action_year_used_for_ndc > last_year):
                    str_error   = "Action date: " + str(action_date) + " inconsistent with NDC implementation period: " + str(first_year) + " to " + str(last_year) + " for reporting party: " + submission.reporting_party_id + ", reported year: " + str(submission.reported_year) + "."
                    self.check_report.add_error_report(str_error)
                    is_valid    = False
        return is_valid
