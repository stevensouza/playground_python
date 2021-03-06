import os
import sys
from string import Template

# from myfunctions import *
# from myfunctions import sayhi, saybye, saylater
# call as: myfunctions.sayhi("steve")
# you can call everything with this approach
from unittest import TestCase

from pandas import DataFrame

import myfunctions
# call as: func.sayhi("steve")
# you can call everything with this approach
import myfunctions as func
from myfunctions import sayhi
# could do this too...
from myfunctions import sayhi as hi
# call as: sayhi("steve")
# you can only call sayhi function with this approach
from person import Person, Child

# basic python syntax experiments
"""
Simple test code of python basics.

To see versions of installed libraries: pip/pip3 freeze
"""


class BasicsTests(TestCase):

    def test_use_class(self):
        me = Person("steve", "souza")
        print(me)
        print(me.get_fname())
        print(me.get_lname())

        my_kid = Child("a", "souza", "purple")
        print(my_kid.get_favorite_color())
        print(my_kid.favorite_color)

    def test_function_module(self):
        print(sayhi("steve"))
        print(myfunctions.sayhi("joel"))
        print(func.sayhi("jean"))
        print(hi("dad"))

    def test_basics(self):
        """my comment"""
        print("\n************* BASICS")
        # python3 myfirstprogram.py
        print("hi")
        print("mom")
        print(sys.version)
        print(10 + 20)
        message = "hi mom"
        print(message.title())
        print(message.lower())
        # format string
        message = f"hi mom {message.upper()}!"
        print(message)
        fname = "steve"
        lname = "souza"
        message = f"{fname} {lname}"
        print(message)
        # no built in constants but all caps by convention
        MY_NUMBER = 14_000_000
        print(MY_NUMBER)
        # Note these are not really booleans. They return a value
        print(1 and 2 and 3)  # 3
        print(1 and 2 or 3)  # 2
        print(1 or 2 and 3 or 4)  # 1
        print(1 and 2 == 2 and 3 or 4)  # 3
        # ternary operator
        my_bool = True
        print(0 if my_bool else 1)  # 0
        print(0 if not my_bool else 1)  # 1

    def test_list_methods(self):
        print("\n************* LIST_METHODS")
        # note strings can be in single or double quotes
        # list=array
        mylist = ["first", 'second', "last"]
        print(mylist)
        print(mylist[0])
        print(mylist[-1])  # last element
        mylist.append("newlast")
        print(mylist[-1])  # last element
        mylist.insert(0, "newfirst")
        del mylist[2]  # remove 'second'
        print(mylist)
        print(mylist.pop())  # removes last item and returns it
        # list.pop(0) would remove first item
        mylist.copy()
        mylist.remove("first")
        mylist.sort()
        mylist.reverse()
        print(sorted(mylist, reverse=True))
        print(mylist)
        newlist = []  # empty list
        print(newlist)
        for item in mylist:
            print(item)
        for value in range(2, 5):
            print(value)
        numlist = list(range(1, 10))
        print(numlist)
        print(min(numlist))
        print(max(numlist))
        print(sum(numlist))
        # list comprehension
        numlist = [value * 10 for value in range(1, 10)]
        print(numlist)
        print(numlist[2:7])
        print(numlist[2:])  # index 2 to end
        print(numlist[:7])  # 0 to 7the item
        print(numlist[:-3])  # 0 to the 3rd from last
        print(numlist[-3:])  # 3rd from end to end
        numlistcopy = numlist[:]
        print(numlistcopy)

        # example of python 'list comprehension' -
        #  for loop and return a new list with each element is a value*2 of each element in numlist.
        new_numlist = [value * 2 for value in numlist]
        print(new_numlist)

        print("both of the following are ways to make the size of the list twice as big")
        new_numlist = new_numlist * 2
        print(new_numlist)
        new_numlist = new_numlist + new_numlist
        print(new_numlist)

    def test_conditionals_method(self):
        print("\n************* CONDITIONALS_METHOD")
        # conditionals
        name = "steve"
        if name == "steve":
            print(f"hi {name}")
        mybool = True
        # can do: and, or
        if (name != "steve" and True):
            print(f"hi {name}")
        elif mybool == False:
            print("won't print")
        else:
            print(f"bye {name}")
        numlist = list(range(1, 10))
        print(numlist)
        if 5 in numlist:
            print("5 is in here")
        if 55 not in numlist:
            print("55 is not in here")

    def test_dictionary_method(self):
        print("\n************* DICTIONARY_METHOD")
        # dictionaries - like a java map i.e key/value pairs
        #  comma on last item is a good practice
        mymap = {5: "joe", 10: "steve", 15: "sandra", }
        print(mymap)
        print(mymap[10])
        mymap[20] = "winnie"
        print(mymap)
        del mymap[20]
        print(mymap)
        print(mymap.get(15))
        print(mymap.get(99))
        print(mymap.get(99, "defaultvalue"))
        emptymap = {}
        print(emptymap)
        print("dictionary keys:values")
        for key, value in mymap.items():
            print(f" key={key}:value={value}")
        print("dictionary keys")
        for key in mymap.keys():
            print(f" key={key}")
        print("dictionary values")
        for value in mymap.values():
            print(f" value={value}")
        # dictionary containing list
        families = {"souza": ["joe", "winnie", "sandra", "jean", "joel", "steve"],
                    "reid": ["william", "jim"],
                    "beck": "jeff"}
        print(families)

    def test_function_method(self):
        print(self._get_souza("steve"))
        print(self._get_souza(name="joe"))
        print(self._get_souza())
        self._varargs("steve", "joe", "bill")

    def test_env_variables(self):
        print(os.environ)
        print(os.environ.get('USER'))
        print(os.environ.get('idonotexist'))
        print(os.environ.get('PATH'))
        print(sys.path, sys.version_info)
        print(sys.version_info)
        #  replace OS variable references with their values.  Can use ${xxx} if no whitespace follows
        template = Template('''
        My template will substitute OS variables in the following: USER=${USER}_HI, HOME=$HOME
        '''
                            )
        mystr = template.substitute(os.environ)
        print(mystr)

    def test_os_commands(self):
        print(os.cpu_count())
        print(os.getlogin())

        print(os.system("ps -e -o time,upr,cpu,command"))
        with os.popen('ps -ef | head -3') as pipe:
            ps_str = pipe.read()
        print(ps_str)

        df = self._ps_to_dataframe()
        print(df)
        print(df.shape)
        print(df.info)
        print(df["COMMAND"].tolist())

    @staticmethod
    def _ps_to_dataframe():
        # the following returns the ps command output as one string with returns after each line
        with os.popen("ps -e -o time,upr,cpu,command") as pipe:
            ps_str = pipe.read()

        # to it to a list with entries as each row returned from the ps command
        ps_rows = ps_str.splitlines()

        # because command can have spaces in it the following will return the command as one and not break it up
        # with its whitespace. i.e return as one string: /usr/sbin/systemstats --daemon. Anything after the 3rd
        # column is grouped as 1 column.  So this will have 4 columns: time,upr,cpu,command
        ps_list = [row.split(maxsplit=3) for row in ps_rows]
        ps_list_header = ps_list.pop(0)
        df = DataFrame(data=ps_list, columns=ps_list_header)
        return df

    # default value of 'steve'
    @staticmethod
    def _get_souza(name="steve"):
        """function comments
            hello my comment
            :rtype: object
        """
        return f"{name} souza"

    @staticmethod
    def _varargs(*names):
        print(names)

# if __name__ == '__main__':
#     basics()
#     list_methods()
#     conditionals_method()
#     dictionary_method()
#     function_method()
#     function_module()
#     use_class()
#     env_variables()
#     os_commands()
