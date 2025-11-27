#II02ActionReportedOnce.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import AEFConsistencyCheck


class II02_ActionReportedOnce(AEFConsistencyCheck):
    """ Verify that the same action for an ITMO is reported only once
        across all relevant reports, tables, and participating Parties.
        An Action is considered the same if they have the same action_date, action_type, action_subtype, party_itmo_registry_id, first_id, and last_id.
        Note that action_subtype is optional, thus may be NULL/empty/None, and is not part of the Action table's primary key.
        Note that if a Party's registry performs the same action
        (transfers or acquires the same block of ITMOs to or from the same acquiring or tranferring Party)
        on the same day, this check will fail, as the AEF specifies a date stamp, not a date-time stamp for actions.
    """

    def __init__(self, submission, cursor):
        super().__init__(submission, cursor)
        return


    def run(self):
        """ Perform the consistency check.
        """
        submission  = self.submission
        actions     = submission.actions  # all cooperative approaches reported by submitting Party
        cursor      = self.cursor
        table_name  = "Actions"
        for action in actions:
#            cursor.execute(f'SELECT action_date FROM {table_name} WHERE action_date = ? AND action_type = ? AND action_subtype = ? AND first_id = ? AND last_id = ?', (action.action_date, action.action_type, action.action_subtype, action.first_id, action.last_id))
            cursor.execute(f'SELECT action_date, action_subtype FROM {table_name} WHERE action_date = ? AND action_type = ? AND party_itmo_registry_id = ? AND first_id = ? AND last_id = ?', (action.action_date, action.action_type, action.party_itmo_registry_id, action.first_id, action.last_id))
            rows    = cursor.fetchall()
            if (len(rows) > 1):
                is_matching_subtype = True
                if (action.action_subtype is None): # need to explicitly match None (python) and NULL (db)
                    for row in rows:
                        if row[1] is not None:
                            is_matching_subtype = False
                            break
                else:
                    for row in rows:
                        if (row[1] == action.action_subtype):
                            is_matching_subtype = False
                            break
                if (is_matching_subtype):
                    print ("\nII02 failed: Action reported more than once: '", action.action_type, "', dated:", action.action_date, ", on ITMO: '", action.first_id, "' - '", action.last_id, "'\n", sep='')
                    return False
        return True


    def report(self):
        """Generate a report of the consistency check."""
        # Placeholder for actual reporting logic
        return
    