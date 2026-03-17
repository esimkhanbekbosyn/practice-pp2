PYTHON
# Practice 5 - Python Regular Expressions

## Objective
In this practice, I learned how to use Python RegEx (regular expressions) with the `re` module.

## What I did
- Used `re.search()` to find first match
- Used `re.findall()` to find all matches
- Used `re.split()` to split text
- Used `re.sub()` to replace text
- Used `re.match()` to match from beginning

## RegEx Topics
- Metacharacters: . ^ $ * + ? [] | ()
- Special sequences: \d \w \s \D \W \S
- Quantifiers: {n} {n,} {n,m}
- Flags: re.IGNORECASE

## Receipt Parsing
I created a script `receipt_parser.py` to parse receipt data.

The program extracts:
- product names
- prices
- total amount
- date and time
- payment method
