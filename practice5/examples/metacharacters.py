import re

# \w  (word characters: letters + digits + _)
txt = "Hello_123 world!"
x = re.findall(r"\w+", txt)
print(x)  # ['Hello_123', 'world']


# \s (spaces)
txt = "Hello world Python"
x = re.findall(r"\s", txt)
print(x)  # [' ', ' ']


# \D (non-digits)
txt = "My number is 12345"
x = re.findall(r"\D", txt)
print(x)  # ['M', 'y', ' ', 'n', 'u', 'm', 'b', 'e', 'r', ' ', 'i', 's', ' ']


# \b (word boundary)
txt = "The rain in Spain"
x = re.findall(r"\bain", txt)
print(x)  # ['ain', 'ain']


# re.search() – тек бірінші match
txt = "I love Python and Python is easy"
x = re.search("Python", txt)
print(x.group())  # Python


# re.split() – бөлу
txt = "apple,banana,orange"
x = re.split(",", txt)
print(x)  # ['apple', 'banana', 'orange']


# re.sub() – ауыстыру
txt = "I like cats"
x = re.sub("cats", "dogs", txt)
print(x)  # I like dogs


# [] + quantifier бірге
txt = "abc123xyz456"
x = re.findall(r"[0-9]+", txt)
print(x)  # ['123', '456']


# email тексеру (қарапайым)
txt = "My email is test123@gmail.com"
x = re.findall(r"\w+@\w+\.\w+", txt)
print(x)  # ['test123@gmail.com']


# () топтау
txt = "Today is 2026-03-19"
x = re.search(r"(\d{4})-(\d{2})-(\d{2})", txt)
print(x.group(1))  # year -> 2026
print(x.group(2))  # month -> 03
print(x.group(3))  # day -> 19