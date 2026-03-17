import re
s=input()
a=re.search(r"\S+@\S+\.\S+",s)
if a:
    print(a.group())
else:
    print('No email')
