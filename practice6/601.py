n=int(input())
a=list(map(int,input().split()))
mp=list(map(lambda x:x*x,a))
count=0
for i in mp:
    count+=i
print(count)