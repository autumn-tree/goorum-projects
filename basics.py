
# formating
data = 3
fmt = f"{data}"
fmtBracket = f"{{data}}"
print("fmt: ", fmt)
print("fmtBracket: ", fmtBracket)

# numeric formating
num = 3
string = f"{num:02d}"
print(string)

num = 3
# minimal total width.formating decimal
string = f"{num:0.2f}"
print(string)

symbol = "BTCUSDT"
print(f"{symbol:10}")

# interning
a = "hello"
b = ["hello", "python"]
print(id(a) == id(b[0]))  # True

a = 3
b = 3
print(a == b)  # True
print(a is b)  # True 

# > 256
a = 1000
b = 1000
print(a == b)  # True
print(a is b)  # False

'''
immutable: int, float, str, tuple -> available for dictionary key
mutable: list, set, dictionary
'''
# list comprehension
even_num = [i for i in range(10) if i % 2 == 0]
print(even_num)  # [0, 2, 4, 6, 8]

odd_num = [i for i in range(10) if i % 2 == 1]
print(odd_num)  # [1, 3, 5, 7, 9]

# pack, both tuples
a = 1, 2
b = (1, 2)
print(a, type(a))  # (1, 2) <class 'tuple'>
print(b, type(b))  # (1, 2) <class 'tuple'>

# unpack
data = (1, 2, 3)
n1, n2, n3 = data
print(n1, n2, n3)  # 1 2 3

scores = (1, 2, 3, 4, 5, 6)
first, *others, last = scores
print(first)
print(others)
print(last)

def hap(n1, n2, n3, n4):
	return n1+n2+n3+n4

scores = scores = (1, 2, 3, 4)
res = hap(*scores)
print(res)

# zip
name = ['merona', 'gugucon']
price = [500, 1000]

z = zip(name, price)
print(z) # zip object


for n, p in z:
	print(n, p) 
	
# empty as zip object z can only be iterated over once
# z is already consumed
zippedList = list(z)
print(zippedList)

# {'merona': 500, 'gugucon': 1000}
zippedDict = dict(zip(name, price))
print(zippedDict)

# namedTuple
from collections import namedtuple
Book = namedtuple('Book', ['title', 'price'])
mybook = Book("Justice", 13)

# "Justice", 13
print(mybook.title, mybook.price)
print(mybook[0], mybook[1])  

def printBook(title, price):
    print(title, price)
    
printBook(*mybook)

