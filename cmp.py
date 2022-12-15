import random
import des


def gen():
    return bin(random.getrandbits(64))[2:].zfill(64)


def desenc(message, key):
    return des.encrypt(message, key)


def desdec(message, key):
    return des.decrypt(message, key)


def xor(a, b):
    return des.xor(a, b)


def G_key(key):
    message_1 = '1'.zfill(64)
    message_2 = '10'.zfill(64)
    return desenc(message_1, key) + desenc(message_2, key)


def PRF_F(message, key):
    return ''.join(G_key(desenc(message, key)))


def ENC(k, x):
    r = gen()
    return [r, xor(PRF_F(r, k), x + ''.zfill(64))]


def ENC_R(k, r, x):
    return xor(PRF_F(r, k), x + ''.zfill(64))


def DEC(k, r, s):
    message = xor(PRF_F(r, k), s)
    tag = message[-64:]
    if sum([int(i) for i in tag]) == 0:
        return message[:64]
    else:
        return None


def AND(ku0, ku1, kv0, kv1, kw0, kw1):
    a = ENC_R(ku0, kv0, kw0)
    b = ENC_R(ku0, kv1, kw0)
    c = ENC_R(ku1, kv0, kw0)
    d = ENC_R(ku1, kv1, kw1)
    ans = [a, b, c, d]
    random.shuffle(ans)
    return ans


def OR(ku0, ku1, kv0, kv1, kw0, kw1):
    a = ENC_R(ku0, kv0, kw0)
    b = ENC_R(ku0, kv1, kw1)
    c = ENC_R(ku1, kv0, kw1)
    d = ENC_R(ku1, kv1, kw1)
    ans = [a, b, c, d]
    random.shuffle(ans)
    return ans


def NOT(ku0, ku1, kw0, kw1):
    a = ENC(ku0, kw1)
    b = ENC(ku1, kw0)
    ans = [a, b]
    random.shuffle(ans)
    return ans
