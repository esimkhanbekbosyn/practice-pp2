# Sets
"""
Set	        Description
[arn]	    Returns a match where one of the specified characters (a, r, or n) is present	
[a-n]	    Returns a match for any lower case character, alphabetically between a and n	
[^arn]	    Returns a match for any character EXCEPT a, r, and n	
[0123]	    Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
[0-9]	    Returns a match for any digit between 0 and 9	
[0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
[a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
[+]	        In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string
"""
# [arn]
import re
txt = "The rain in Spain"
# Check if the string has any a, r, or n characters:
x = re.findall("[arn]", txt)
print(x) # ['r', 'a', 'n', 'n', 'a', 'n']

# [a-n]
txt = "The rain in Spain"
# Check if the string has any characters between a and n:
x = re.findall("[a-n]", txt)
print(x) # ['h', 'e', 'a', 'i', 'n', 'i', 'n', 'a', 'i', 'n']

# [^arn]
txt = "The rain in Spain"
# Check if the string has other characters than a, r, or n:
x = re.findall("[^arn]", txt)
print(x) # ['T', 'h', 'e', ' ', 'i', ' ', 'i', ' ', 'S', 'p', 'i']

# [0123]
txt = "The rain in Spain"
# Check if the string has any 0, 1, 2, or 3 digits:
x = re.findall("[0123]", txt) # []
print(x) 

# [0-9]
txt = "8 times before 11:45 AM"
# Check if the string has any digits:
x = re.findall("[0-5]", txt)
print(x) # ['1','1','4','5']

# [a-zA-Z]
txt = "8 times before 11:45 AM"
# Check if the string has any characters from a to z lower case, and A to Z upper case:
x = re.findall("[a-zA-Z]", txt)
print(x) # ['t', 'i', 'm', 'e', 's', 'b', 'e', 'f', 'o', 'r', 'e', 'A', 'M']

# [+]
txt = "8 times before 11:45 AM"
# Check if the string has any + characters:
x = re.findall("[+]", txt)
print(x) # []