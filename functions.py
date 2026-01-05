import math 

def safe_sqrt(x):
    try: 
        return math.sqrt(x)
    except ValueError:
        return "You cannot square root a negative number"

double = lambda x: x * 2

print(safe_sqrt(9))
print(safe_sqrt(-1))
print(double(5))
