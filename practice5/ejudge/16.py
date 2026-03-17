import re
s=input()
m=re.search(r"Name:(.*), Age: (\d+)",s)
if m:
    print(m.group(1),m.group(2))