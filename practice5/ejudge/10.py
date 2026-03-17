import re
s=input()
if re.findall(r"dog|cat",s):
    print("Yes")
else:
    print("No")