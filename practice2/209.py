n=int(input())
a=list(map(int,input().split()))
mx=a[0]
mn=a[0]
for i in range(n):
    if a[i]>mx:
        mx=a[i]
    if a[i]<mn:
        mn=a[i]
for i in range(n):
    if a[i]==mx:
        a[i]=mn
for x in a:
    print(x,end=' ')
