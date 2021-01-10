import sys

# basic python syntax experiments


def basics():
    """my comment"""
    print("\n************* BASICS")
    # python3 helloworld.py
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


def list_methods():
    global value, numlist
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
    print(mylist.pop())  # removes last item
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


def conditionals_method():
    global numlist
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


def dictionary_method():
    global value
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


def function_method():
    print(_get_souza("steve"))
    print(_get_souza(name="joe"))
    print(_get_souza())
    _varargs("steve", "joe", "bill")


# default value of 'steve'
def _get_souza(name="steve"):
    """function comments
        hello my comment
        :rtype: object
    """
    return f"{name} souza"


def _varargs(*names):
    print(names)


basics()
list_methods()
conditionals_method()
dictionary_method()
function_method()
