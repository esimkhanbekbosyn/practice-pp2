n=int(input())
a=list(map(int,input().split()))
f=list(filter(lambda x:x%2==0,a))
print(len(f))
