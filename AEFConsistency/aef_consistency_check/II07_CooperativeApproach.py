#II07_CooperativeApproach.py

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II07_CooperativeApproach(AEFConsistencyCheck):
    """ Verify the cooperative approach of ITMOs are consistent.
        Since the cooperative approach identifier is part of an ITMO's unique identifier,
        this check verifies the cooperative approach identifier declared in actions and holdings
        match that of the ITMOs in the action or holding.
    """


    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II07: Cooperative Approach of ITMOs are consistent")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        is_valid    = True
        itmo_tuples = self.get_itmo_tuples()
        for itmo_tuple in itmo_tuples:
            ca_id       = itmo_tuple[1]
            first_id    = itmo_tuple[3]
            last_id     = itmo_tuple[4]
            if (ca_id != first_id[0:6]):
                if (len(itmo_tuple) == 8):  # itmo from an action
                    str_error   = "ITMOs: '" + first_id + "' - '" + last_id + "' in Action on: " + str(itmo_tuple[7])[0:10] + " inconsistent with declared cooperative approach id: '" + ca_id + "'"
                else:   # itmo from a holding
                    str_error   = "ITMOs: '" + first_id + "' - '" + last_id + "' in Holding is inconsistent with declared cooperative approach id: '" + ca_id + "'"
                self.check_report.add_error_report(str_error)
                is_valid    = False
                continue
        return is_valid
