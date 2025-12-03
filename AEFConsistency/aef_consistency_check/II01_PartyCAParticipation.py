#II01PartyCAParticipation.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *


class II01_PartyCAParticipation(AEFConsistencyCheck):
    """ Verify that a Party only reports actions and holdings derived from
        cooperative approaches in which the Party participates.
    """

    def __init__(self, submission, cursor):
        super().__init__(submission, cursor)
        return


    def run(self):
        """ Perform the consistency check.
        """
        submission          = self.submission
        submitting_party_id = submission.party_id
        ca_ids              = self.get_reported_cooperative_approach_ids()  # all cooperative approaches reported by submitting Party
        for ca_id in ca_ids:
            auth_party_ids  = self.get_authorizing_party_ids(ca_id)     # the Parties authorizing the cooperative approach
            part_party_ids  = self.get_participating_party_ids(ca_id)   # the Parties participating in the cooperative approach
            party_ids       = set(auth_party_ids + part_party_ids)
            if (submitting_party_id not in party_ids):
                print ("\nII01 failed: '", submitting_party_id, "' reports on cooperative approach: '", ca_id, "' for which it does not participate.\n")
                return False
        return True


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


    def report(self):
        """Generate a report of the consistency check."""
        # Placeholder for actual reporting logic
        return