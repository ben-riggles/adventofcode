from functools import reduce
import math

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def euclidean(a: int, b: int, c: int) -> int:
    gcd = math.gcd(a, b)
    k = int(c/gcd)
    q, r, s, t = [0,0], [a,b], [1,0], [0,1]
    
    while r[-1] != 0:
        quotient = r[-2] / r[-1]
        q.append(math.floor(quotient) if quotient >=0 else math.ceil(quotient))
        r.append(r[-2] - q[-1] * r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])

    s, t = s[-2], t[-2]
    if a*s + b*t == -gcd:
        k = -k
    return s*k


x = euclidean(63, -13, -6)
print(x)
y = math.lcm(63, 13)
print(y)
z = int(63) * x + 6
print(z)
print(z % y)