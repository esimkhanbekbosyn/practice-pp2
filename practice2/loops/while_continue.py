#1
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)

#2
x = 0
while x < 4:
    x += 1
    if x == 2:
        continue
    print(x)

#3
n = 0
while n < 3:
    n += 1
    continue

#4
i = 1
while i <= 5:
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1
