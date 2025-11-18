# create_db.py

import sqlite3
import re
from openpyxl import load_workbook


def create_tables(db_path):
    """Create the AEF consistency database at 'db_path'."""

    conn	= sqlite3.connect(db_path)
    cursor	= conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Submissions (
        party_Id                TEXT not null,
        reported_year           INTEGER not null,
        major_version           INTEGER not null,
        minor_version           INTEGER not null,
        date_of_submission      TEXT not null,
        consistency_status      TEXT,
        ndc_period_start_year   INTEGER,
        ndc_period_end_year     INTEGER,
        PRIMARY KEY (party_Id, reported_year, major_version, minor_version)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Authorizations (
        auth_id                     TEXT not null,
        date                        REAL not null,
        version                     INTEGER not null,
        cooperative_approach_id     TEXT,
        authorised_quantity         INTEGER,
        metric                      TEXT,
        applicable_gwp_values       TEXT,
        applicable_nonghg_metric    TEXT,
        sectors                     TEXT,
        activity_types              TEXT,
        purposes_for_auth           TEXT,
        authorized_parties          TEXT,
        authorized_entities         TEXT,
        oimp_authorized             TEXT,
        authorized_timeframe        TEXT,
        auth_tcs                    TEXT,
        auth_documentation          TEXT,
        first_transfer_defn4oimp    TEXT,
        reporting_party_Id          TEXT not null,
        reported_year               INTEGER not null,
        major_version               INTEGER not null,
        minor_version               INTEGER not null,
        PRIMARY KEY (auth_id, date, version),
        FOREIGN KEY (reporting_party_Id, reported_year, major_version, minor_version)
            REFERENCES Submissions(party_Id, reported_year, major_version, minor_version)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Actions (
        action_date                 REAL not null,
        action_type                 TEXT not null,
        action_subtype              TEXT,
        cooperative_approach_id     TEXT,
        authorization_id            TEXT,
        first_transferring_party_id TEXT,
        party_itmo_registry_id      TEXT not null,
        first_id                    TEXT not null,
        last_id                     TEXT not null,
        underlying_unit_registry_id TEXT,
        first_unit_id               TEXT,
        last_unit_id                TEXT,
        metric                      TEXT,
        applicable_gwp_values       TEXT,
        applicable_nonghg_metric    TEXT,
        quantity                    INTEGER,
        quantity_nonghg_metric      INTEGER,
        mitigation_type             TEXT,
        vintage                     INTEGER,
        transferring_party_id       TEXT,
        acquiring_party_id          TEXT,
        oimp_purpose                TEXT,
        use_cancelling_party_id     TEXT,
        use_cancelling_entity_id    TEXT,
        year_used_for_NDC           INTEGER,
        consistency_results         TEXT,
        additional_info             TEXT,
        reporting_party_Id          TEXT not null,
        reported_year               INTEGER not null,
        major_version               INTEGER not null,
        minor_version               INTEGER not null,
        PRIMARY KEY (action_date, action_type, party_itmo_registry_id, first_id, last_id),
        FOREIGN KEY (reporting_party_Id, reported_year, major_version, minor_version)
            REFERENCES Submissions(party_Id, reported_year, major_version, minor_version)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Holdings (
        cooperative_approach_id     TEXT,
        authorization_id            TEXT,
        first_transferring_party_id TEXT,
        party_itmo_registry_id      TEXT,
        first_id                    TEXT,
        last_id                     TEXT,
        underlying_unit_registry_id TEXT,
        first_unit_id               TEXT,
        last_unit_id                TEXT,
        metric                      TEXT,
        applicable_gwp_values       TEXT,
        applicable_nonghg_metric    TEXT,
        quantity                    INTEGER,
        quantity_nonghg_metric      INTEGER,
        mitigation_type             TEXT,
        vintage                     INTEGER,
        reporting_party_Id          TEXT not null,
        reported_year               INTEGER not null,
        major_version               INTEGER not null,
        minor_version               INTEGER not null,
        PRIMARY KEY (reporting_party_Id, reported_year, major_version, minor_version, party_itmo_registry_id, first_id, last_id),
        FOREIGN KEY (reporting_party_Id, reported_year, major_version, minor_version)
            REFERENCES Submissions(party_Id, reported_year, major_version, minor_version)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Authorized_Entities (
        date_of_authorization       REAL not null,
        name_of_entity              TEXT,
        country_of_incorporation    TEXT,
        identification_number       TEXT,
        cooperative_approach_id     TEXT,
        conditions                  TEXT,
        change_revoc_conditions     TEXT,
        additional_info             TEXT,
        reporting_party_Id          TEXT not null,
        reported_year               INTEGER not null,
        major_version               INTEGER not null,
        minor_version               INTEGER not null,
        PRIMARY KEY (date_of_authorization, name_of_entity, cooperative_approach_id, reporting_party_Id, reported_year, major_version, minor_version),
        FOREIGN KEY (reporting_party_Id, reported_year, major_version, minor_version)
            REFERENCES Submissions(party_Id, reported_year, major_version, minor_version)
    );
    """)
    conn.commit()
    return conn