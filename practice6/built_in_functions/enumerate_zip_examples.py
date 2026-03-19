names = ["Ali", "Dana", "Aruzhan"]
scores = [90, 85, 95]
ages = ["18", "19", "20"]

# enumerate()
print("=== enumerate() example ===")
for index, name in enumerate(names, start=1):
    print(index, name)

# zip()
print("\n=== zip() example ===")
for name, score in zip(names, scores):
    print(name, score)

# Type checking
print("\n=== type checking ===")
print(type(names))
print(type(scores))
print(type(ages[0]))

# Type conversion
print("\n=== type conversion ===")
ages_int = list(map(int, ages))
print("Converted ages:", ages_int)

score_float = float(scores[0])
print("First score as float:", score_float)

number_str = str(123)
print("Number to string:", number_str)