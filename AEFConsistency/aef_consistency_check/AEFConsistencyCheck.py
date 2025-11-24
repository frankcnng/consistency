#AEFConsistencyCheck.py

class AEFConsistencyCheck:
    """Abstract superclass for consistency checks of AEF files.
    These checks are describedin the Article 6.2 Reference Manual (version 3, 2025)"""

    def __init__(self):
        return
    
    def check(self, cursor):
        """Perform the consistency check using the provided database cursor.
        This method should be overridden by subclasses."""
        return
    
    def report(self):
        """Generate a report of the consistency check.
        This method should be overridden by subclasses."""
        return
    