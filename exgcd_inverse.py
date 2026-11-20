def exgcd(a , b):
  if b == 0:
    return a , 1 , 0

  g , x1 , y1 = exgcd(b , a%b)

  x = y1
  y = x1 - (a//b)*y1
  return g , x , y

def inverse(a , m):
  g , x , y = exgcd(a , m)
  if g != 1:
    return -1

  return x%m
