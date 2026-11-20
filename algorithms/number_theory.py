"""整數運算；不透過浮點數計算模反元素或因數分解。"""


def gcd(a, b):
    """Euclid，O(log min(|a|,|b|))；gcd(0,0)=0。"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """回傳 (g,x,y)，使 ax+by=g>=0；O(log min(|a|,|b|))。"""
    old_r, r, old_x, x, old_y, y = a, b, 1, 0, 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return (old_r, old_x, old_y) if old_r >= 0 else (-old_r, -old_x, -old_y)


def modular_inverse(a, modulus):
    """模反元素；不互質或 modulus<=1 時拋錯。"""
    if modulus <= 1:
        raise ValueError('modulus must exceed one')
    divisor, x, _ = extended_gcd(a, modulus)
    if divisor != 1:
        raise ValueError('inverse does not exist')
    return x % modulus


def modular_power(base, exponent, modulus):
    """平方乘法，O(log exponent)；指數非負且模數為正。"""
    if exponent < 0 or modulus <= 0:
        raise ValueError('invalid exponent or modulus')
    result, base = 1 % modulus, base % modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent //= 2
    return result


def sieve(limit):
    """Eratosthenes，列出 <=limit 的質數；O(n log log n) time/O(n) space。"""
    if limit < 2:
        return []
    prime = bytearray([1]) * (limit + 1)
    prime[0] = prime[1] = 0
    p = 2
    while p * p <= limit:
        if prime[p]:
            for multiple in range(p * p, limit + 1, p):
                prime[multiple] = 0
        p += 1
    return [value for value, yes in enumerate(prime) if yes]


def factorize(number):
    """試除法回傳 {質因數:次方}，number>=1；O(sqrt n)。"""
    if number < 1:
        raise ValueError('positive integer required')
    factors, divisor = {}, 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor
        divisor += 1
    if number > 1:
        factors[number] = factors.get(number, 0) + 1
    return factors


def chinese_remainder(congruences):
    """廣義 CRT，輸入 (remainder,modulus)；回傳 (x,lcm)，不相容拋錯。"""
    value, period = 0, 1
    for remainder, modulus in congruences:
        if modulus <= 0:
            raise ValueError('positive modulus required')
        divisor, inverse, _ = extended_gcd(period, modulus)
        difference = remainder - value
        if difference % divisor:
            raise ValueError('inconsistent congruences')
        step = difference // divisor * inverse % (modulus // divisor)
        value += period * step
        period *= modulus // divisor
        value %= period
    return value, period
