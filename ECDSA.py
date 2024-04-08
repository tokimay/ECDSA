from hashlib import sha256
import secp256k1


def sign(message: str, privateKey: str) -> tuple[int, int]:
    if privateKey.startswith('0x') or privateKey.startswith('0X'):
        privateKey = privateKey[2:]
    p = int(privateKey, 16)
    h = int((sha256(message.encode('utf-8')).hexdigest()), 16)
    k = h + p  # random number
    # r = k mod p
    # r = rx
    r = secp256k1.multipy(repeat=k, point=secp256k1.g())
    r = r[0] % secp256k1.n()
    if r == 0:
        return sign(message, privateKey)
    k_inverse = pow(k, -1, secp256k1.n())
    s = k_inverse * (h + r * p) % secp256k1.n()
    return r, s


def verify(signature: tuple, message: str, public_key: tuple) -> bool:
    (r, s) = signature
    h = int((sha256(message.encode('utf-8')).hexdigest()), 16)
    s_inverse = pow(s, -1, secp256k1.n())
    # c = ((h * s_inverse) * G) + ((r * s_inverse) * publicKey)
    u = h * s_inverse % secp256k1.n()
    v = r * s_inverse % secp256k1.n()
    p1 = secp256k1.multipy(repeat=v, point=public_key)
    p2 = secp256k1.multipy(repeat=u, point=secp256k1.g())
    c = secp256k1.add(p1, p2)
    return c[0] == r
