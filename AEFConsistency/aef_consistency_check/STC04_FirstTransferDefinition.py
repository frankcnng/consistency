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
        is_valid        = True
        cursor          = self.cursor
        submission      = self.submission
        party_id        = submission.party_id
        actions         = submission.actions

        for action in actions:
            if (action.action_type == "First transfer"):
                action_subtype  = action.action_subtype
                action_date     = action.action_date[0:10]
                auth_id         = action.authorization_id
                if (action_subtype is None):
                    str_error   = "First transfer action must specify an action subtype for action on: " + action_date + "."
                    self.check_report.add_error_report(str_error)
                    is_valid    = False
                    continue
                if (action_subtype == "First international transfer"): # if it's a first international transfer, ensure the acquiring Party is a different Party
                    acquiring_party_id   = action.acquiring_party_id
                    if ((acquiring_party_id is None) or (acquiring_party_id == party_id)):
                        str_error   = "First international transfer action must specify a different acquiring Party ID for action on: " + action_date + "."
                        self.check_report.add_error_report(str_error)
                        is_valid    = False
                    continue
                else: # if it's not a first international transfer, it must be use or cancellation for OIMP
                    cursor.execute(f'SELECT purposes_for_auth, first_transfer_defn4oimp  FROM {self.authorizations_table_name} WHERE authorization_id = ?', (auth_id, ))
                    db_row          = cursor.fetchone()
                    db_purpose      = db_row[0] if (db_row is not None) else "N/A"
                    db_1xfer_defn   = db_row[1] if (db_row is not None) else "N/A"
                    if ("OIMP" in db_purpose):
                        if (action_subtype != db_1xfer_defn):
                            self.check_report.add_error_report("First transfer action on " + action_date + " has subtype: '" + action_subtype + "' not consistent with first transfer definition for OIMP in authorization:" + auth_id + "' is defined as: '" + db_1xfer_defn + "'.")
                            is_valid    = False
                    else:
                        self.check_report.add_error_report("First transfers that are not first international transfers must be authorised for OIMP, authorization:" + auth_id + "' is authorized for: '" + db_purpose + "'.")
                        is_valid    = False
        return is_valid
