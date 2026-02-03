#1
a=int(input())
while a%2==0:
    a//=2
if a==1:
    print('YES')
else:
    print("NO")

#2
n=int(input())
a=1
while a<=n:
    print(a, end=' ') 
    a*=2

#3
i=1
while i<=5:
    print(i)
    i+=1
