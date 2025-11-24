#aef_submission.py

"""Module defining classes representing the AEF submission object.
Each AEFSubmission object corresponds to a single AEFSubmission worksheet.
The consistency checks are performed on this object, against itself,
and data in the database.
"""

class AEFSubmission:
    """Class representing an AEF submission."""

    def __init__(self, party_id, reported_year, major_version, minor_version, date_of_submission):
        self.party_id               = party_id
        self.reported_year          = reported_year
        self.major_version          = major_version
        self.minor_version          = minor_version
        self.date_of_submission     = date_of_submission
        self.authorizations         = []
        self.actions                = []
        self.holdings               = []
        self.authorized_entities    = []
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

 
class AEFAuthorization:
    """Class representing an AEF authorization."""

    def __init__(self, auth_id, date, version, reporting_party_id, reported_year, major_version, minor_version):
        self.auth_id                = auth_id
        self.date                   = date
        self.version                = version
        self.reporting_party_id     = reporting_party_id
        self.reported_year          = reported_year
        self.major_version          = major_version
        self.minor_version          = minor_version
        self.submission             = None
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

    def __init__(self, action_date, action_type, auth_id, date, version, reporting_party_id, reported_year, major_version, minor_version):
        self.action_date            = action_date
        self.action_type            = action_type
        self.auth_id                = auth_id
        self.date                   = date
        self.version                = version
        self.reporting_party_id     = reporting_party_id
        self.reported_year          = reported_year
        self.major_version          = major_version
        self.minor_version          = minor_version
        self.submission             = None
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

    def __init__(self, holding_id, quantity, metric, reporting_party_id, reported_year, major_version, minor_version):
        self.holding_id             = holding_id
        self.quantity               = quantity
        self.metric                 = metric
        self.reporting_party_id     = reporting_party_id
        self.reported_year          = reported_year
        self.major_version          = major_version
        self.minor_version          = minor_version
        self.submission             = None
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

    def __init__(self, entity_id, name, reporting_party_id, reported_year, major_version, minor_version):
        self.entity_id              = entity_id
        self.name                   = name
        self.reporting_party_id     = reporting_party_id
        self.reported_year          = reported_year
        self.major_version          = major_version
        self.minor_version          = minor_version
        self.submission             = None
        return

    def load_to_db(self, cursor):
        """Load the authorized entity into the database using the provided cursor."""
        cursor.execute("""
            INSERT INTO Authorized_Entities (entity_id, name, reporting_party_Id, reported_year, major_version, minor_version)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.entity_id, self.name, self.reporting_party_id, self.reported_year, self.major_version, self.minor_version))
        return
    
