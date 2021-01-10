import sys
# python3 helloworld.py
print("hi")
print("mom")
print(sys.version)
print(10+20)
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

# note strings can be in single or double quotes
# list=array
mylist = ["first", 'second', "last"]
print(mylist)
print(mylist[0])
print(mylist[-1]) # last element
mylist.append("newlast")
print(mylist[-1]) # last element
mylist.insert(0, "newfirst")
del mylist[2] # remove 'second'
print(mylist)
print(mylist.pop()) # removes last item
mylist.remove("first")
mylist.sort()
mylist.reverse()

print(sorted(mylist, reverse=True))

print(mylist)
newlist=[] # empty list

for item in mylist:
    print(item)

for value in range(2,5):
    print(value)

numlist = list(range(1, 10))
print(numlist)
print(min(numlist))
print(max(numlist))
print(sum(numlist))

# list comprehension
numlist = [value*10 for value in range(1,10)]
print(numlist)
print(numlist[2:7])
print(numlist[2:]) # index 2 to end
print(numlist[:7]) # 0 to 7the item
print(numlist[:-3]) # 0 to the 3rd from last
print(numlist[-3:]) # 3rd from end to end

numlistcopy = numlist[:]
print(numlistcopy)

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

numlist = list(range(1,10))
print(numlist)
if 5 in numlist:
    print("5 is in here")

if 55 not in numlist:
    print("55 is not in here")


# dictionaries - like a java map i.e key/value pairs
map = {5,10,15}
print(map)