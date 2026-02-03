a=int(input())
n=list(map(int,input().split()))
mx=n[0]
idx=0
for i in range(1,a):
    if n[i]>mx:
        mx=n[i]
        idx=i
print(idx+1)