"""
- CSV file reading
- Regular expressions (email + log parsing)
- Matplotlib simple graph
- Pytest unit test
- Multiprocessing
"""

# csv file
import csv

def read_csv_example(filename):
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("CSV file not found")


# regular expressions
import re
def extract_emails(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return re.findall(pattern, text)

def extract_error_codes(log_text):
    return re.findall(r"ERROR\[(\d+)\]", log_text)


# matplot
import matplotlib.pyplot as plt

def draw_simple_graph():
    x = [1, 2, 3, 4]
    y = [10, 20, 15, 30]

    plt.plot(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Simple Line Chart")
    plt.show()


# multi processing
from multiprocessing import Pool

def square(x):
    return x * x

def multiprocessing_example():
    with Pool(4) as p:
        result = p.map(square, [1, 2, 3, 4])
    print("Multiprocessing result:", result)


# pytest
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5


# main execution
if __name__ == "__main__":
    # CSV example
    read_csv_example("data.csv")

    # Regex examples
    sample_text = "Contact: test.user@gmail.com or admin@company.co.kr"
    print("Emails:", extract_emails(sample_text))

    log = "ERROR[404]: Not Found | ERROR[500]: Server Error"
    print("Error codes:", extract_error_codes(log))

    # Graph example
    draw_simple_graph()

    # Multiprocessing example
    multiprocessing_example()
