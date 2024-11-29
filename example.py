import secp256k1
import ECDSA


message = "Hello cryptography"
privateKey = 0x636678001c32339343b4ffadf02d1818e8a545926eebfdcf01f2b0f8573575c4
publicKey = secp256k1.compressed_public_key(privateKey)

r, s = signature = ECDSA.sign(message, privateKey)
print(f"r = {r}")
print(f"s = {s}")
print(f"Is verified? {ECDSA.verify(signature, message, publicKey)}")
