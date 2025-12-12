#II06_UsingPartiesEntities.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II06_UsingPartiesEntities(AEFConsistencyCheck):
    """ Verify that the using Party/entity or entities align with their authorization, as applicable.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II06: Using Parties/entities align with their authorization.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
        """
        cursor      = self.cursor
        submission  = self.submission
        actions     = submission.actions
        is_valid    = True
        for action in actions:
            if (action.action_type == "Use"):
                auth_id         = action.authorization_id
                first_id        = action.first_id
                last_id         = action.last_id
                using_party     = action.use_cancelling_party_id
                using_entity    = action.use_cancelling_entity_id
                if (using_party) is None:
                    self.check_report.add_error_report("Using Party not defined for using: '" + first_id + "' - '" + last_id + "' on " + str(action.action_date))
                    is_valid    = False
                else:
                    cursor.execute(f'SELECT cooperative_approach_id, reporting_party_id, authorized_parties, authorized_entities FROM {self.authorizations_table_name} WHERE authorization_id = ?', (auth_id, ))
                    db_rows = cursor.fetchall()
                    authorized_parties  = set()
                    authorized_entities = set()
                    for db_row in db_rows:
                        authorized_parties.add(db_row[1])
                        if (db_row[2] is not None):
                            list_parties    = [item.strip() for item in db_row[2].split(',')]
                            authorized_parties.update(list_parties)
                        if ((using_entity is not None) and (db_row[3] is not None)):
                            list_entities    = [item.strip() for item in db_row[3].split(',')]
                            authorized_entities.update(list_entities)
                    if (using_party in authorized_parties) is False:
                        self.check_report.add_error_report("Using Party: '" + using_party + "' is not authorized to use these ITMOs: '" + first_id + "' - '" + last_id + "'")
                        is_valid    = False
                    if (using_entity is not None):
                        if ((len(authorized_entities) > 0) and (using_entity in authorized_entities)) is False:
                            self.check_report.add_error_report("Using entity: '" + using_entity + "' is not authorized to use these ITMOs: '" + first_id + "' - '" + last_id + "'")
                            is_valid    = False
                            continue
        return is_valid
