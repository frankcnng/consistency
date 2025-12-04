#AEFConsistencyCheck.py


import aef_submission


class AEFConsistencyCheck:
    """ Abstract superclass for consistency checks of AEF files.
        These checks are describedin the Article 6.2 Reference Manual (version 3, 2025)
    """

    def __init__(self, submission, cursor):
        
        self.submission = submission
        self.cursor     = cursor
        return


    def run(self):
        """Perform the consistency check using the provided database cursor.
        This method should be overridden by subclasses."""
        return True


    def report(self):
        """Generate a report of the consistency check.
        This method should be overridden by subclasses."""
        return


    def get_itmo_tuples(self):
        """ Return a list of ITMO tuples from this submission's actions and holdings,
            consisting of the ITMOBlock, ca_id, metric, first_id, last_id from the action or holding.
        """
        submission  = self.submission
        actions     = submission.actions
        holdings    = submission.holdings
        itmo_tuples = []
        itmo_tuples.extend(self.get_itmo_tuples_from_list(actions))
        itmo_tuples.extend(self.get_itmo_tuples_from_list(holdings))
        return itmo_tuples
    

    def get_itmo_tuples_from_list(self, list):
        """ Return a list of ITMO tuples from this submission's list.
            List is either the submissions actions or holdings.
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
            This is also the list of cooperative approach ids of all reported ITMOs in this submission.
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