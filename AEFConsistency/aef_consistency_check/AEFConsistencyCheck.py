#AEFConsistencyCheck.py

class AEFConsistencyCheck:
    """Abstract superclass for consistency checks of AEF files.
    These checks are describedin the Article 6.2 Reference Manual (version 3, 2025)"""

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
    