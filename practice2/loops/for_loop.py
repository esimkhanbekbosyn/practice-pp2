#1
a=int(input())
n=list(map(int,input().split()))
s=0
for i in range(a):
    if n[i]>=0:
        s+=1
print(s)

#2
a=int(input())
n=list(map(int,input().split()))
mx=n[0]
for i in range(1,a):
    if n[i]>mx:
        mx=n[i]
print(mx)

#3
a=int(input())
n=list(map(int,input().split()))
mx=n[0]
idx=0
for i in range(1,a):
    if n[i]>mx:
        mx=n[i]
        idx=i
print(idx+1)

#4
for x in "banana":
  print(x)