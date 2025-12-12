#II07_CooperativeApproach.py

import sqlite3

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *


class II07_CooperativeApproach(AEFConsistencyCheck):
    """ Verify that the cooperative approach of an ITMO is consistent across 
        all relevant reports, tables and participating Parties.
    """

    def __init__(self, submission, cursor):
        super().__init__(submission, cursor)
        return
