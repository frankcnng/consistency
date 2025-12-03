#AEFConsistencyCheck.py

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