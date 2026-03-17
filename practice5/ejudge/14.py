import re
s=input()
p=re.compile(r"^\d+$")
if p.match(s):
    print('Match')
else:
    print('No match')