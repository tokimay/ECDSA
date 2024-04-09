import secp256k1
import ECDSA


message = "Hello"
privateKey = 69906862961406275191037665143949518378358884783178670810968073317421786058782
publicKeyCoordinate = secp256k1.getPublicKeyCoordinate(privateKey)

r, s = signature = ECDSA.sign(message, hex(privateKey))
print(f"r = {r}")
print(f"s = {s}")
print(ECDSA.verify(signature, message, publicKeyCoordinate))
