#II01PartyCAParticipation.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II01_PartyCAParticipation(AEFConsistencyCheck):
    """ Verify that a Party only reports actions and holdings derived from
        cooperative approaches in which the Party participates.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II01: Party only reports actions and holdings derived from cooperative approaches in which the Party participates.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        submission          = self.submission
        submitting_party_id = submission.party_id
        ca_ids              = self.get_reported_cooperative_approach_ids()  # all cooperative approaches reported by submitting Party
        is_valid            = True
        for ca_id in ca_ids:
            auth_party_ids  = self.get_authorizing_party_ids(ca_id)     # the Parties authorizing the cooperative approach
            part_party_ids  = self.get_participating_party_ids(ca_id)   # the Parties participating in the cooperative approach
            party_ids       = set(auth_party_ids + part_party_ids)
            if (submitting_party_id not in party_ids):
                self.check_report.add_error_report("'" + submitting_party_id + "' reports on cooperative approach: '" + ca_id + "' for which it does not participate.")
                is_valid    = False
        return is_valid


    def get_authorizing_party_ids(self, cooperative_approach_id):
        """ Return a list of party_ids that authorised the
            the cooperative approach with cooperative_approach_id.
        """
        cursor      = self.cursor
        table_name  = "Authorizations"
        cursor.execute(f'SELECT reporting_party_Id FROM {table_name} WHERE cooperative_approach_id = ?', (cooperative_approach_id, ))
        rows	    = cursor.fetchall()
        party_ids = []
        for row in rows:
            columns  = row
            for column in columns:
                party_ids.append(column)
        return list(set(party_ids))


    def get_participating_party_ids(self, cooperative_approach_id):
        """ Return a list of party_ids are authorized to participate in
            the cooperative approach with cooperative_approach_id.
        """
        cursor      = self.cursor
        table_name  = "Authorizations"
        cursor.execute(f'SELECT authorized_parties FROM {table_name} WHERE cooperative_approach_id = ?', (cooperative_approach_id, ))
        rows	    = cursor.fetchall()
        party_ids = []
        for row in rows:
            columns  = row
            for column in columns:
                column  = column.replace(" ", "")
                party_ids.extend(column.split(","))
        return list(set(party_ids))
