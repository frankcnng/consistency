#aef_submission.py

"""Module defining classes representing the AEF submission object.
Each AEFSubmission object corresponds to a single AEFSubmission worksheet.
The consistency checks are performed on this object, against itself,
and data in the database.
"""

import re
import sqlite3
from openpyxl import load_workbook

import datetime

#from aef_consistency_check import *

from aef_consistency_check.II01_PartyCAParticipation import II01_PartyCAParticipation
from aef_consistency_check.II02_ActionReportedOnce import II02_ActionReportedOnce
from aef_consistency_check.II03_SectorsActivityTypes import II03_SectorsActivityTypes
from aef_consistency_check.II04_Metrics import II04_Metrics
from aef_consistency_check.II05_UnderlyingUnitBlocks import II05_UnderlyingUnitBlocks
from aef_consistency_check.II06_UsingPartiesEntities import II06_UsingPartiesEntities


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
        self.ndc_period_first_year  = db_row[7]
        self.ndc_period_last_year   = db_row[8]
        self.str_path               = db_row[9]
        self.load_authorizations(cursor)
        self.load_actions(cursor)
        self.load_holdings(cursor)
        self.load_auth_entities(cursor)
        return


    def get_submission_key(self):
        """Return the primary key of the submission as a tuple."""
        return (self.party_id, self.reported_year, self.major_version, self.minor_version)


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


    def check_consistency(self, cursor, report):
        """ Perform consistency checks on the submission.
        """
        is_valid    = True
        check   = II01_PartyCAParticipation(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        check   = II02_ActionReportedOnce(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        check   = II03_SectorsActivityTypes(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        check   = II04_Metrics(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        check   = II05_UnderlyingUnitBlocks(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        check   = II06_UsingPartiesEntities(self, cursor, report)
        if (check.run()) is False:
            is_valid    = False
        workbook    = load_workbook(self.str_path, data_only=True)
        report.print(workbook, is_valid)
        workbook.save(self.str_path)
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

    
class CooperativeApproach:
    pass


class ITMOBlock:
    """ Class representing a block of ITMOs
    """
    def __init__(self, str_first_id, str_last_id):
        self.regexp         = r"(CA\d{4}-[A-Z]{3}\d{2}-[A-Z]{3}-)([1-9]\d{0,2}((\d*)|(,\d{3})*))(-\d{4})"
        str0, str1, str2    = self.split_itmo_id(str_first_id)
        first_nonsequence   = str0+str2
        block_first         = int(str1.replace(",",""))
        str0, str1, str2    = self.split_itmo_id(str_last_id)
        last_nonsequence    = str0+str2
        block_last          = int(str1.replace(",",""))
        if (first_nonsequence == last_nonsequence):
            if (block_first <= block_last):
                self.start_nonsequence  = first_nonsequence
                self.block_first        = block_first
                self.last_nonsequence   = last_nonsequence
                self.block_last         = block_last
                return
            else:   # Proposed block's start id is greater than end id
                raise InvalidITMOBlockException("Start ITMO id: '", str_first_id, "' > end ITMO id: '", str_last_id, "'.")
        else:   # Nonsequence number parts of the start and end ITMOs do not match
            raise InvalidITMOBlockException("Start: '", str_first_id, "' and end '", str_last_id, "' ITMO ids do not match")


    def is_overlapping(self, itmo_block):
        """ Return true is this block overlaps with itmo_block.
            Assume that both this object, and itmo_block are valid ITMO blocks
        """
        if (self.start_nonsequence == itmo_block.start_nonsequence):    #blocks may overlap, if they're from the same CA, Party, Registry, Vintage
            x_first0, x_last0, x_first1, x_last1    = self.block_first, self.block_last, itmo_block.block_first, itmo_block.block_last
            x_first_overlap                         = max(x_first0, x_first1)
            x_last_overlap                          = min(x_last0, x_last1)
            return (x_first_overlap <= x_last_overlap)
        else:
            return False


    def split_itmo_id(self, str_itmo_id):
        """ Return the three parts of itmo_id: before sequence number, sequence number, after sequence number.
            itmo_id should always match the regular expression, as submission has been syntax checked.
            The Exception should never be raised.
        """
        pattern = re.compile(self.regexp)
        match   = pattern.match(str_itmo_id)
        if (match):
            str0    = match.group(1)
            str1    = match.group(2)
            str2    = match.group(match.lastindex)
            return str0, str1, str2
        else:
            raise InvalidITMOBlockException("Invalid ITMO id: '", str_itmo_id, "'.")


class InvalidITMOBlockException(Exception):
    """ Attempt to create an ITMO block with invalid pairing of start_id and end_id.
        Either the non-sequence number parts of the start_id and end_id do not match,
        or the start_id is greater than the end_id.
    """
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"InvalidITMOBlockException: {self.message}"