#II05_UnderlyingUnitBlocks.py

import sqlite3
from difflib import SequenceMatcher

import aef_submission

from aef_consistency_check.AEFConsistencyCheck import *
from aef_consistency_check.AEFConsistencyReport import AEFCheckReport


class II05_UnderlyingUnitBlocks(AEFConsistencyCheck):
    """ Verify that the underlying unit blocks 'Start/End IDs' (when present)
        are consistent across all relevant reports, tables and participating Parties.
    """

    def __init__(self, submission, cursor, submission_report):
        self.check_report = AEFCheckReport("II05: Underlying unit blocks' 'Start/End IDs' are consistent.")
        submission_report.add_check_report(self.check_report)
        super().__init__(submission, cursor, submission_report)
        return


    def run(self):
        """ Perform the consistency check.
            For each ITMO block in the submission, validate underlying unit blocks (when present) are consistent.
            This means, for each overlapping ITMO block, the underlying unit block ranges are consistent.
        """
        cursor              = self.cursor
        action_table_name   = "Actions"
        holdings_table_name = "Holdings"
        itmo_tuples = self.get_itmo_tuples()

        cursor.execute(f'SELECT first_id, last_id, first_unit_id, last_unit_id, reporting_party_Id, reported_year, major_version, minor_version FROM {action_table_name}')
        db_rows = cursor.fetchall()
        cursor.execute(f'SELECT first_id, last_id, first_unit_id, last_unit_id, reporting_party_Id, reported_year, major_version, minor_version FROM {holdings_table_name}')
        db_rows.extend(cursor.fetchall())
        is_valid    = True
        for itmo_tuple in itmo_tuples:  # for each ITMO block in submission
            itmo_block, first_id, last_id, first_unit_id, last_unit_id   = itmo_tuple[0], itmo_tuple[3], itmo_tuple[4], itmo_tuple[5], itmo_tuple[6]

            if (((first_unit_id is None) != (last_unit_id is None)) or ((first_unit_id == "NA") != (last_unit_id == "NA"))): # if underlying units declared without matching NULL start or end ids.
                self.check_report.add_error_report("ITMO with inconsistent underlying units: '" + first_id + "' - '" + last_id + "' underlying units with invalid start-end id pair.")
                self.check_report.add_error_report("/tUnderlying units: '" + (first_unit_id or "") + "' - '" + (last_unit_id or ""))
                is_valid    = False
                continue
            if ((first_unit_id is not None) and (first_unit_id != "NA")): #if underlying units is not null
                try:
                    blocks   = self.underlying_block(first_unit_id, last_unit_id)
                    underlying_first, underlying_last, underlying_pre, underlying_post   = blocks[0][0], blocks[0][1], blocks[0][2], blocks[0][3]
                except Exception as e:
                    self.check_report.add_error_report("ITMO with invalid underlying units: '" + first_id + "' - '" + last_id + "', underlying units: '" + first_unit_id + "' - '" + last_unit_id + "'")
                    self.check_report.add_error_report("\tApart from the sequence number, first unit id and last unit id must be exactly the same.")
                    is_valid    = False
                    continue
                else:
                    pass

            # This block of code compares the metrics for each overlapping itmo block in all submissions
            for db_row in db_rows:      # for each row from db's actions and holdings tables
                db_first_id, db_last_id, db_first_unit_id, db_last_unit_id    = db_row[0], db_row[1], db_row[2], db_row[3]
                if ((first_unit_id is None) and (last_unit_id is None) and (db_first_unit_id is None) and (db_last_unit_id is None)):
                    continue
                if ((first_unit_id == "NA") and (last_unit_id == "NA") and (db_first_unit_id == "NA") and (db_last_unit_id == "NA")):
                    continue
                try:
                    db_itmo_block   = aef_submission.ITMOBlock(db_first_id, db_last_id)    # get the ITMO block from the db row
                except aef_submission.InvalidITMOBlockException as e:
                    self.check_report.add_error_report(str(e))
                    is_valid    = False
                else:
                    if (itmo_block.is_overlapping(db_itmo_block)):   # if the itmo_block from the db the overlapping (some ITMOs are the same) as the itmo_block from the submission
                        if ((first_unit_id is None) and (db_first_unit_id is None) and (last_unit_id is None) and (db_last_unit_id is None)):  # if both blocks do not declare underlying units, no need to check
                            continue
                        if (((first_unit_id is not None) and (last_unit_id is not None) and (db_first_unit_id is not None) and (db_last_unit_id is not None)) is False): # if underlying units declared inconsistently with overlapping block
                            self.check_report.add_error_report("ITMO with inconsistent underlying units: '" + first_id + "' - '" + last_id + "'")
                            self.check_report.add_error_report("\tvs: '" + db_first_id + "' - '" + db_last_id + "' in Submission: " + db_row[4] + " " + str(db_row[5]) + " version " + str(db_row[6]) + "." + str(db_row[7]))
                            is_valid    = False
                            continue
                        try:
                            db_blocks   = self.underlying_block(db_first_unit_id, db_last_unit_id)
                            db_underlying_first, db_underlying_last, db_underlying_pre, db_underlying_post   = db_blocks[0][0], db_blocks[0][1], db_blocks[0][2], db_blocks[0][3]
                        except Exception as e:
                            self.check_report.add_error_report("Overlapping ITMO with invalid underlying units: '" + first_id + "' - '" + last_id + "', underlying units: '" + first_unit_id + "' - '" + last_unit_id)
                            self.check_report.add_error_report("\tOverlapping ITMO: '" + db_first_id + "' - '" + db_last_id + "', underlying units: '" + db_first_unit_id + "' - '" + db_last_unit_id + "' in Submission: " + db_row[4] + " " + str(db_row[5]) + " version " + str(db_row[6]) + "." + str(db_row[7]))
                            self.check_report.add_error_report("\tApart from the sequence number, first unit id and last unit id must be exactly the same.")
                            is_valid    = False
                            continue
                        else:
                            if (((underlying_pre == db_underlying_pre) and (underlying_post == db_underlying_post)) is False):  # if the words around the sequence do not match
                                self.check_report.add_error_report("ITMO with inconsistent underlying units: '" + first_id + "' - '" + last_id + "', underlying units: '" + first_unit_id + "' - '" + last_unit_id)
                                self.check_report.add_error_report("\tvs: '" + db_first_id + "' - '" + db_last_id + "', underlying units: '" + db_first_unit_id + "' - '" + db_last_unit_id + "' in Submission: " + db_row[4] + " " + str(db_row[5]) + " version " + str(db_row[6]) + "." + str(db_row[7]))
                                is_valid    = False
                                continue
                            # if the overlap of the underlying blocks to not match the offsets of the ITMO blocks
                            if (((db_itmo_block.block_first - itmo_block.block_first) == (db_underlying_first - underlying_first)) and ((db_itmo_block.block_last - itmo_block.block_last) == (db_underlying_last - underlying_last)) is False):
                                self.check_report.add_error_report("ITMO with inconsistent underlying units: '" + first_id + "' - '" + last_id + "', underlying units: '" + first_unit_id + "' - '" + last_unit_id)
                                self.check_report.add_error_report("\tvs: '" + db_first_id + "' - '" + db_last_id + "', underlying units: '" + db_first_unit_id + "' - '" + db_last_unit_id + "' in Submission: " + db_row[4] + " " + str(db_row[5]) + " version " + str(db_row[6]) + "." + str(db_row[7]))
                                is_valid    = False
                                continue
        return is_valid


    def underlying_block(self, underlying_first_id, underlying_last_id):
        """
        Return the first and end sequence numbers from the underlying unit start and and underlying end id.
        Since the format of ids for underlying units is undefined, the constant and inconstant parts of the id is used to determine the sequence number.
        
        :param self: This check
        :param underlying_first_id: String sequence number from the first underlying unit of the block
        :param underlying_last_id: String sequence number of the last underlying unit of the block
        """
        blocks   = []
        matcher = SequenceMatcher(None, underlying_first_id, underlying_last_id)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "equal":
                blocks.append((int(underlying_first_id[i1:i2]), int(underlying_last_id[j1:j2]), underlying_first_id[0:i1-1], underlying_first_id[i2 + 1:len(underlying_first_id)]))
        return blocks