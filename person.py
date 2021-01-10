class Person:
    """A class to represent a person"""

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname
