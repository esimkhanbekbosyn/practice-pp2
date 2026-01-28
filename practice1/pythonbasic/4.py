#global variable
x = 'awesome' #global
def myfunc():
  x = 'fantastic' #local
myfunc()
print('Python is ' + x)