#STC02_AuthorizedUsage.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *


class STC02_AuthorizedUsage(AEFConsistencyCheck):
    """ Verify the authorization of an ITMO is consistent with the actual usage.
    """

    def __init__(self, submission, cursor):
        super().__init__(submission, cursor)
        return


    def run(self):
        """Perform the consistency check using the provided database cursor."""
        # Placeholder for actual consistency checking logic
        return True