import re

# re.I (IGNORECASE)
txt = "Python PYTHON python"
print(re.findall("python", txt, re.I))
# ['Python', 'PYTHON', 'python']


# re.M (MULTILINE)
txt = """Start
middle
Start again"""
print(re.findall("^Start", txt, re.M))
# ['Start', 'Start']


# re.S (DOTALL)
txt = "Hello\nWorld"
print(re.findall("Hello.World", txt, re.S))
# ['Hello\nWorld']


# re.A (ASCII)
txt = "Café 123"
print(re.findall(r"\w+", txt, re.A))
# ['Caf', '123']


# re.U (UNICODE - default in Python 3)
txt = "Café 123"
print(re.findall(r"\w+", txt))
# ['Café', '123']


# re.X (VERBOSE) – readable pattern
txt = "My number is 12345"
pattern = r"""
\d+      # one or more digits
"""
print(re.findall(pattern, txt, re.X))
# ['12345']


# Combine flags
txt = """Hello
python
Python"""
print(re.findall("^python", txt, re.I | re.M))
# ['python', 'Python']


# re.sub with flags
txt = "I like PYTHON"
x = re.sub("python", "Java", txt, flags=re.I)
print(x)
# I like Java


# re.search with flags
txt = "Welcome to PYTHON world"
x = re.search("python", txt, re.I)
print(x.group())
# PYTHON
