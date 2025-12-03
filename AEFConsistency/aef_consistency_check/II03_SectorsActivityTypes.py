#II03_SectorsActivityTypes.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *


class II03_SectorsActivityTypes(AEFConsistencyCheck):
    """ Verify that the sectors and activity types for each ITMO remain consistent
        throughout their lifecycle and across all relevant reports, tables, and participating Parties.
    """

    def __init__(self, submission, cursor):
        super().__init__(submission, cursor)
        return


    def run(self):
        """ Perform the consistency check using the provided database cursor.
        """
        cursor              = self.cursor
        action_table_name   = "Actions"
        holdings_table_name = "Holdings"
        itmo_tuples = self.get_itmo_tuples()

        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric FROM {action_table_name}')
        db_rows = cursor.fetchall()
        cursor.execute(f'SELECT cooperative_approach_id, first_id, last_id, metric FROM {holdings_table_name}')
        db_rows.extend(cursor.fetchall())

        authorizations_table_name   = "Authorizations"
        db_ca_ids  = [] # list of all cooperative approach ids
        for itmo_tuple in itmo_tuples:  # for each ITMO block in submission
            block, ca_id, metric   = itmo_tuple[0], itmo_tuple[1], itmo_tuple[2]
            
            # This block gets the sectors and activity types for the cooperative approach in the submission's authorizations
            authorizations  = self.submission.authorizations    # get the authorizations for the ca_id of this itmo block
            sectors         = []
            activity_types  = []
            is_ca_in_auths  = False
            for authorization in authorizations:
                if (authorization.cooperative_approach_id == ca_id):
                    is_ca_in_auths  = True
                    auth_sectors  = authorization.sectors
                    if (auth_sectors is not None):
                        sectors.extend([str_sector.strip() for str_sector in auth_sectors.split(",")]) # get sectors of the cooperative approach
                    auth_activity_types  = authorization.activity_types
                    if (auth_activity_types is not None):
                        activity_types.extend([str_activity_type.strip() for str_activity_type in auth_activity_types.split(",")]) # get activity_types of the cooperative approach
            sectors         = set(sectors)
            activity_types  = set(activity_types)
            if (is_ca_in_auths is False):   # if cooperative approach has not authorisation in this submission, there are no associated sectors and activity types to check.
                continue

            for db_row in db_rows:      # for each row from db's actions and holdings tables
                db_ca_id, db_first_id, db_last_id, db_metric    = db_row[0], db_row[1], db_row[2], db_row[3]
                try:
                    itmo_block  = aef_submission.ITMOBlock(db_first_id, db_last_id)    # get the ITMO block from the db row
                except aef_submission.InvalidITMOBlockException as e:
                    print(e)
                else:
                    if (block.is_overlapping(itmo_block)):  # if the block from the db the overlapping (some ITMOs are the same) as the block from the submission

                        # get the sectors and activity types associated with db_ca_id and compare them with the sectors and activity types of ca_id
                        # verification will fail if the sectors and activity types do not match
                        cursor.execute(f'SELECT sectors, activity_types FROM {authorizations_table_name} WHERE cooperative_approach_id = ?', (db_ca_id, ))
                        db_auth_rows = cursor.fetchall()
                        for db_auth_row in db_auth_rows:
                            str_db_sectors, str_db_activity_types  = db_auth_row[0], db_auth_row[1]
                            if (str_db_sectors is not None):
                                db_sectors  = [str_sector.strip() for str_sector in str_db_sectors.split(",")]
                            if (str_db_activity_types is not None):
                                db_activity_types  = [str_activity_types.strip() for str_activity_types in str_db_activity_types.split(",")]                                    
                        db_sectors          = set(db_sectors)
                        db_activity_types   = set(db_activity_types)

                        # all sectors and activity types for db_ca_id are in db_sectors and db_activity_types
                        # all sectors and activity types for ca_id in submission are in sectors and activity_types
                        inconsistent_sectors    = db_sectors ^ sectors
                        inconsistent_activity_types = db_activity_types ^ activity_types
                        if (len(inconsistent_sectors) > 0):
                            print("\nII03 failed: ITMO with inconsistent sectors: '", itmo_tuple[3], "' - '", itmo_tuple[4], "'", sep='')
                            print(sectors)
                            print(db_sectors)
                            return False
                        if (len(inconsistent_activity_types) > 0):
                            print("\nII03 failed: ITMO with inconsistent activity_types: '", itmo_tuple[3], "' - '", itmo_tuple[4], "'", sep='')
                            print(activity_types)
                            print(db_activity_types)
                            return False
                    else:
                        continue
        return True


    def report(self):
        """Generate a report of the consistency check."""
        # Placeholder for actual reporting logic
        return
    

    def get_itmo_tuples(self):
        """
        """
        submission  = self.submission
        actions     = submission.actions
        holdings    = submission.holdings
        itmo_tuples = []
        itmo_tuples.extend(self.get_itmo_tuples_from_list(actions))
        itmo_tuples.extend(self.get_itmo_tuples_from_list(holdings))
        return itmo_tuples
        """
        for action in actions:
            try:
                itmo_block  = ITMOBlock(action.first_id, action.last_id)
            except InvalidITMOBlockException as e:
                print(e)
            else:
                ca_id   = action.cooperative_approach_id
                metric  = action.metric
                itmo_blocks.append((itmo_block, ca_id, metric))
        for holding in holdings:
            try:
                itmo_block  = ITMOBlock(holding.first_id, holding.last_id)
            except InvalidITMOBlockException as e:
                print(e)
            else:
                ca_id   = holding.cooperative_approach_id
                metric  = holding.metric
                itmo_blocks.append((itmo_block, ca_id, metric))
        return itmo_blocks
        """
    

    def get_itmo_tuples_from_list(self, list):
        """
        """
        tuples  = []
        for item in list:
            try:
                first_id, last_id   = item.first_id, item.last_id
                itmo_block          = aef_submission.ITMOBlock(first_id, last_id)
            except aef_submission.InvalidITMOBlockException as e:
                print(e)
            else:
                ca_id   = item.cooperative_approach_id
                metric  = item.metric
                tuples.append((itmo_block, ca_id, metric, first_id, last_id))   
        return tuples


    def get_reported_cooperative_approach_ids(self):
        """ Return a list of unique cooperative approach ids in this submission's actions and holdings.
        """
        submission  = self.submission
        actions     = submission.actions
        holdings    = submission.holdings
        ca_ids      = []
        for action in actions:
            ca_id = action.cooperative_approach_id
            if ca_id in ca_ids:
                continue
            else:
                ca_ids.append(ca_id)
        for holding in holdings:
            ca_id = holding.cooperative_approach_id
            if ca_id in ca_ids:
                continue
            else:
                ca_ids.append(ca_id)
        return list(set(ca_ids))