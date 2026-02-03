a=int(input())
n=list(map(int,input().split()))
s=0
for i in range(a):
    if n[i]>=0:
        s+=1
print(s)