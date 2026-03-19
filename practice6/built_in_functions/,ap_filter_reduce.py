from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map(): square numbers
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter(): keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

# reduce(): sum all numbers
total = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce:", total)

# Other built-in functions
print("Length:", len(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Sum:", sum(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))