#aef_submission.py

"""Module defining classes representing the AEF submission object.
Each AEFSubmission object corresponds to a single AEFSubmission worksheet.
The consistency checks are performed on this object, against itself,
and data in the database.
"""

import sqlite3

import datetime

#from aef_consistency_check import *

from aef_consistency_check.II01_PartyCAParticipation import II01_PartyCAParticipation
from aef_consistency_check.II02_ActionReportedOnce import II02_ActionReportedOnce


class AEFSubmission:
    """Class representing an AEF submission."""

    def __init__(self, cursor, db_row):
        self.party_id               = db_row[0]
        self.reported_year          = db_row[1]
        self.major_version          = db_row[2]
        self.minor_version          = db_row[3]
        self.date_of_submission     = db_row[4]
        self.review_status          = db_row[5]
        self.consistency_status     = db_row[6]
        self.ndc_period_start_year  = db_row[7]
        self.ndc_period_end_year    = db_row[8]
        self.load_authorizations(cursor)
        self.load_actions(cursor)
        self.load_holdings(cursor)
        self.load_auth_entities(cursor)
        return


    def get_submission_key(self):
        """Return the primary key of the submission as a tuple."""
        return (self.party_id, self.reported_year, self.major_version, self.minor_version)


    def load_to_db(self, cursor):
        """Load the submission into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Submissions (party_id, reported_year, major_version, minor_version, date_of_submission)
            VALUES (?, ?, ?, ?, ?)
        """, (self.party_id, self.reported_year, self.major_version, self.minor_version, self.date_of_submission))
        return


    def load_authorizations(self, cursor):
        """Load all authorizations associated with this submission from the database."""
        cursor.execute("""
            SELECT * FROM Authorizations
            WHERE reporting_party_Id = ? AND reported_year = ? AND major_version = ? AND minor_version = ?
            """, (self.party_id, self.reported_year, self.major_version, self.minor_version))
        db_rows = cursor.fetchall()
        self.authorizations = []
        for db_row in db_rows:
            authorization = AEFAuthorization(self, db_row)
            self.authorizations.append(authorization)
        return


    def load_actions(self, cursor):
        """Load all actions associated with this submission from the database."""
        cursor.execute("""
            SELECT * FROM Actions
            WHERE reporting_party_Id = ? AND reported_year = ? AND major_version = ? AND minor_version = ?
            """, (self.party_id, self.reported_year, self.major_version, self.minor_version))
        db_rows = cursor.fetchall()
        self.actions = []
        for db_row in db_rows:
            action = AEFAction(self, db_row)
            self.actions.append(action)
        return


    def load_holdings(self, cursor):
        """Load all holdings associated with this submission from the database."""
        cursor.execute("""
            SELECT * FROM Holdings
            WHERE reporting_party_Id = ? AND reported_year = ? AND major_version = ? AND minor_version = ?
            """, (self.party_id, self.reported_year, self.major_version, self.minor_version))
        db_rows = cursor.fetchall()
        self.holdings = []
        for db_row in db_rows:
            holding = AEFHolding(self, db_row)
            self.holdings.append(holding)
        return


    def load_auth_entities(self, cursor):
        """Load all authorized entities associated with this submission from the database."""
        cursor.execute("""
            SELECT * FROM Authorized_Entities
            WHERE reporting_party_Id = ? AND reported_year = ? AND major_version = ? AND minor_version = ?
            """, (self.party_id, self.reported_year, self.major_version, self.minor_version))
        db_rows = cursor.fetchall()
        self.authorized_entities = []
        for db_row in db_rows:
            authorised_entity = AEFAuthorizedEntity(self, db_row)
            self.authorized_entities.append(authorised_entity)
        return


    def check_consistency(self, cursor):
        """Perform consistency checks on the submission."""
        # Placeholder for consistency check logic

        check   = II01_PartyCAParticipation(self, cursor)
        check   = II02_ActionReportedOnce(self, cursor)
        check.run()

        return

 
class AEFAuthorization:
    """Class representing an AEF authorization."""

    def __init__(self, submission, db_row):
        self.authorization_id           = db_row[0]
        self.date_of_authorization      = db_row[1]
        self.version_of_authorization   = db_row[2]
        self.cooperative_approach_id    = db_row[3]
        self.authorised_quantity        = db_row[4]
        self.metric                     = db_row[5]
        self.applicable_gwp_values      = db_row[6]
        self.applicable_nonghg_metric   = db_row[7]
        self.sectors                    = db_row[8]
        self.activity_types             = db_row[9]
        self.purposes_for_auth          = db_row[10]
        self.authorized_parties         = db_row[11]
        self.authorized_entities        = db_row[12]
        self.oimp_authorized            = db_row[13]
        self.authorized_timeframe       = db_row[14]
        self.auth_tcs                   = db_row[15]
        self.auth_documentation         = db_row[16]
        self.first_transfer_defn4oimp   = db_row[17]
        self.reporting_party_id         = db_row[18]
        self.reported_year              = db_row[19]
        self.major_version              = db_row[20]
        self.minor_version              = db_row[21]
        self.submission                 = submission
        return


    def load_to_db(self, cursor):
        """Load the authorization into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Authorizations (auth_id, date, version, reporting_party_Id, reported_year, major_version, minor_version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.auth_id, self.date, self.version, self.reporting_party_id, self.reported_year, self.major_version, self.minor_version))
        return


class AEFAction:
    """Class representing an AEF action."""

    def __init__(self, submission, db_row):
        self.action_date                    = db_row[0]
        self.action_type                    = db_row[1]
        self.action_subtype                 = db_row[2]
        self.cooperative_approach_id        = db_row[3]
        self.authorization_id               = db_row[4]
        self.first_transferring_party_id    = db_row[5]
        self.party_itmo_registry_id         = db_row[6]
        self.first_id                       = db_row[7]
        self.last_id                        = db_row[8]
        self.underlying_unit_registry_id    = db_row[9]
        self.first_unit_id                  = db_row[10]
        self.last_unit_id                   = db_row[11]
        self.metric                         = db_row[12]
        self.applicable_gwp_values          = db_row[13]
        self.applicable_nonghg_metric       = db_row[14]
        self.quantity                       = db_row[15]
        self.quantity_nonghg_metric         = db_row[16]
        self.mitigation_type                = db_row[17]
        self.vintage                        = db_row[18]
        self.first_transferring_party_id    = db_row[19]
        self.acquiring_party_id             = db_row[20]
        self.oimp_purpose                   = db_row[21]
        self.use_cancelling_party_id        = db_row[22]
        self.use_cancelling_entity_id       = db_row[23]
        self.year_used_for_ndc              = db_row[24]
        self.consistency_results            = db_row[25]
        self.additional_info                = db_row[26]
        self.reporting_party_id             = db_row[27]
        self.reported_year                  = db_row[28]
        self.major_version                  = db_row[29]
        self.minor_version                  = db_row[30]
        self.submission                     = submission
        return


    def load_to_db(self, cursor):
        """Load the action into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Actions (action_date, action_type, auth_id, date, version, reporting_party_Id, reported_year, major_version, minor_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.action_date, self.action_type, self.auth_id, self.date, self.version, self.reporting_party_id, self.reported_year, self.major_version, self.minor_version))
        return


class AEFHolding:
    """Class representing an AEF holding."""

    def __init__(self, submission, db_row):
        self.cooperative_approach_id        = db_row[0]
        self.authorization_id               = db_row[1]
        self.first_transferring_party_id    = db_row[2]
        self.party_itmo_registry_id         = db_row[3]
        self.first_id                       = db_row[4]
        self.last_id                        = db_row[5]
        self.underlying_unit_registry_id    = db_row[6]
        self.first_unit_id                  = db_row[7]
        self.last_unit_id                   = db_row[8]
        self.metric                         = db_row[9]
        self.applicable_gwp_values          = db_row[10]
        self.applicable_nonghg_metric       = db_row[11]
        self.quantity                       = db_row[12]
        self.quantity_nonghg_metric         = db_row[13]
        self.mitigation_type                = db_row[14]
        self.vintage                        = db_row[15]
        self.reporting_party_id             = db_row[16]
        self.reported_year                  = db_row[17]
        self.major_version                  = db_row[18]
        self.minor_version                  = db_row[19]
        self.submission                     = submission
        return


    def load_to_db(self, cursor):
        """Load the holding into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Holdings (holding_id, quantity, metric, reporting_party_Id, reported_year, major_version, minor_version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.holding_id, self.quantity, self.metric, self.reporting_party_id, self.reported_year, self.major_version, self.minor_version))
        return


class AEFAuthorizedEntity:
    """Class representing an AEF authorized entity."""

    def __init__(self, submission, db_row):
        self.date_of_authorization      = db_row[0]
        self.name_of_entity             = db_row[1]
        self.country_of_incorporation   = db_row[2]
        self.identification_number      = db_row[3]
        self.cooperative_approach_id    = db_row[4]
        self.conditions                 = db_row[5]
        self.change_revoc_conditions    = db_row[6]
        self.additional_info            = db_row[7]
        self.reporting_party_id         = db_row[8]
        self.reported_year              = db_row[9]
        self.major_version              = db_row[10]
        self.minor_version              = db_row[11]
        self.submission                 = submission        
        return


    def load_to_db(self, cursor):
        """Load the authorized entity into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Authorized_Entities (entity_id, name, reporting_party_Id, reported_year, major_version, minor_version)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.entity_id, self.name, self.reporting_party_id, self.reported_year, self.major_version, self.minor_version))
        return
    
class CooperativeApproach:
    pass