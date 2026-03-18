import re

# \w (word characters: letters, digits, _)
txt = "Hello_123 world!"
print(re.findall(r"\w", txt))
# ['H','e','l','l','o','_','1','2','3','w','o','r','l','d']

print(re.findall(r"\w+", txt))
# ['Hello_123', 'world']


# \W (non-word characters)
txt = "Hello@# world!"
print(re.findall(r"\W", txt))
# ['@', '#', ' ', '!']


# \S (non-space characters)
txt = "Hi there!"
print(re.findall(r"\S", txt))
# ['H','i','t','h','e','r','e','!']


# \Z (end of string)
txt = "I love Spain"
print(re.findall(r"Spain\Z", txt))
# ['Spain']

print(re.findall(r"love\Z", txt))
# []


# Combine patterns
txt = "User123 logged in at 2026"
print(re.findall(r"\w+\d+", txt))
# ['User123']


# Find phone number (simple)
txt = "Call me at 87051234567"
print(re.findall(r"\d{11}", txt))
# ['87051234567']


# First non-digit character
txt = "1234abc567"
x = re.search(r"\D", txt)
print(x.group())
# 'a'


# First space position
txt = "Hello World Python"
x = re.search(r"\s", txt)
print(x.start())
# 5


# First word
txt = "Python is cool"
x = re.search(r"\w+", txt)
print(x.group())
# Python