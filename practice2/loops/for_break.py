#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
#2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#3
for i in range(5):
    if i == 3:
        break
    print(i)

#4
for x in [1, 2, 3, 4]:
    if x == 2:
        break
    print(x)
