#STC03_NDCImplementationPeriod.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class STC03_NDCImplementationPeriod(AEFConsistencyCheck):
    """ For ITMOs used towards NDC,
        verify the MOs are used within the same NDC implementation period as when they occurred.
    """


    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("STC03: MOs used within the same NDC implementation period.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        is_valid    = True
        submission  = self.submission
        actions     = submission.actions
        first_year  = submission.ndc_period_first_year
        last_year   = submission.ndc_period_last_year

        for action in actions:
            if ((action.action_type == "Use") and ("NDC" in action.purpose)):
                action_date                 = action.action_date
                action_year_used_for_ndc    = action.year_used_for_ndc
                if (action_year_used_for_ndc < first_year or action_year_used_for_ndc > last_year):
                    str_error   = "For Action on " + action_date[0:10] + ", year used towards NDC: " + str(action_year_used_for_ndc) + " is inconsistent with NDC implementation period: " + str(first_year) + " to " + str(last_year) + "."
                    self.check_report.add_error_report(str_error)
                    is_valid    = False
        return is_valid
