class Person:
    """A class to represent a person"""

    # constructor
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        self.nationality = "usa" # default value

    # class functions are called methods. functions are stan alone
    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname


class Child(Person):

    def __init__(self, fname, lname, favorite_color):
        super().__init__(fname, lname)
        self.favorite_color = favorite_color

    def get_favorite_color(self):
        return self.favorite_color