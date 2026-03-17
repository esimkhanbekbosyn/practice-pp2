import re
s=input()
p=r"\d{2}/\d{2}/\d{4}"
print(len(re.findall(p,s)))
