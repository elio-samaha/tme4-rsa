def exp(a, n, p):
    res = 1
    N = n
    A = a
    while N>0:
        if N%2 == 1: 
            res =(res*A)%p
        A = (A*A)%p 
        N = N//2
    return res

def rsa_chiffrement (x,N,e):
    return exp(x, e, N)

def rsa_dechiffrement (y,p,q,d):
    return exp(y,d,p*q)

def bezout(a, b):
    u0,v0, u1,v1, r0,r1 = 1,0,0,1, a, b
    while r1 != 0:
        qi = r0 // r1
        u0,u1 = u1, u0 - qi*u1
        v0,v1 = v1, v0 - qi*v1
        r0, r1 = r1, r0 - qi*r1
    return r0, u0, v0

# Retourne s tel que s % n1 == a1 et s % n2 == a2
def crt2 (a1,a2,n1,n2):
    _, u,v = bezout(n1,n2)
    return (a2*n1*u + a1*n2*v)%(n1*n2) , 1

def rsa_dechiffrement_crt (y,p,q,up,uq,dp,dq,N):
    xp = exp(y,dp,p)
    xq = exp(y,dq,q)
    return (xp*up + xq*uq) %N

#### Wiener
def cfrac(a,b):
    li = []
    while b != 0:
        li.append(a//b)
        a,b = b , a%b
    return li

def reduite(L):
    k = [L[0] , L[0]*L[1] + 1]
    d = [1 , L[1]]
    for i in range(1 , len(L) - 1): 
        k.append(k[i] * L[i+1] + k[i-1])
        d.append(d[i] * L[i+1] + d[i-1])
    return (k,d)

def Wiener(m,c,N,e):
    L = cfrac(e,N)
    (k,d) = reduite(L)
    for i in range(len(d)):
        x = pow(c , d[i] , int(N))
        if x == m:
            return d[i]
    return -1

### Generation de premiers
import random
def is_probable_prime(N, nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.
    """

    def miller(a, n):
        """
        Returns True if a proves that n is composite, False if n is probably prime in base n
        """

        def decompose(i, k=0):
            """
            decompose(n) returns (s,d) st. n = 2**s * d, d odd
            """
            if i % 2 == 0:
                return decompose(i // 2, k + 1)
            else:
                return (k, i)

        (s, d) = decompose(n - 1)
        x = pow(a, d, n)
        if (x == 1) or (x == n - 1):
            return False
        while s > 1:
            x = pow(x, 2, n)
            if x == n - 1:
                return False
            s -= 1
        return True

    if N == 2:
        return True
    for i in range(nbases):
        import random
        a = random.randint(2, N - 1)
        if miller(a, N):
            return False
    return True


def random_probable_prime(bits):
    """
    Returns a probable prime number with the given number of bits.
    Remarque : on est sur qu'un premier existe par le postulat de Bertrand
    """
    n = 1 << bits
    import random
    p = random.randint(n, 2 * n - 1)
    while (not (is_probable_prime(p))):
        p = random.randint(n, 2 * n - 1)
    return p
