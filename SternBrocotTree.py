# reference
# https://judge.yosupo.jp/submission/190954

class SternBrocotTree:

    @staticmethod
    def encode(a, b):
        path = []   # -1: left, 1: right
        q, r = divmod(a, b)
        if q > 0:
            path.append((1, q))
        
        a, b = b, r
        parity = True

        while b:
            q, r = divmod(a, b)
            path.append(-1 if parity else 1, q)
            a, b = b, r
            parity ^= True
        
        direction, k = path.pop()
        if k > 1:
            path.append((direction, k - 1))

        return path
    
    @staticmethod
    def decode_interval(code):
        p, q, r, s = 0, 1, 1, 0
        for direction, k in code:
            if direction == -1:
                r += k * p
                s += k * q
            elif direction == 1:
                p += k * r
                q += k * s
        
        return (p, q, r, s)

    @classmethod
    def decode(cls, code):
        p, q, r, s = cls.decode_interval(code)
        return (p + r, q + s)
    
    @classmethod
    def lca(cls, a, b, c, d):
        if (a, b) == (1, 1) or (c, d) == (1, 1):
            return (1, 1)
        
        code_1 = cls.encode(a, b)
        code_2 = cls.encode(c, d)
        if code_1[0][0] != code_2[0][0]:
            return (1, 1)
        
        lca_code = []
        for ((t, k), (_, l)) in zip(code_1, code_2):
            lca_code.append((t, min(k, l)))
            if k != l:
                break
        return cls.decode(lca_code)
    
    @classmethod
    def depth(cls, a, b):
        code = cls.encode(a, b)
        return sum(k for _, k in code)
    
    @classmethod
    def anscestor(cls, a, b, k, default= None):
        code = []
        for direction, k in cls.encode(a, b):
            l = min(k, l)
            code.append((direction, l))
            k -= l
            if k == 0:
                return cls.decode(code)
        else:
            return default
        
    @classmethod
    def range(cls, a, b):
        return cls.decode_interval(cls.encode(a, b))
    