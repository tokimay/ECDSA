import ECDSA
import secp256k1

privateKey = 0x636678001c32339343b4ffadf02d1818e8a545926eebfdcf01f2b0f8573575c4

x = secp256k1.public_key_coordinate(privateKey)[0]
print('x=', x)

y = secp256k1.public_key_coordinate(privateKey)[1]
print('y=', y)

c = secp256k1.compressed_public_key(privateKey)
print('c(hex)  =', c)

uc = secp256k1.uncompressed_public_key(privateKey)
print('uc(hex) =', uc)

uc2 = secp256k1.de_compressed(int(c, 16))
print('uc2(hex)=', uc2)

print(uc == uc2)

print(secp256k1.public_key_coordinate(privateKey) == secp256k1.recover_public_key_coordinate(int(c, 16)))
print(secp256k1.public_key_coordinate(privateKey) == secp256k1.recover_public_key_coordinate(int(uc, 16)))

