# Elliptic Curve Cryptography
### ECC

ECC is commonly used for cryptology purposes. </br>
It focuses on asymmetric cryptography using pairs of public and private keys. </br>
This type of cryptography is used for encryption and decryption of data, authentication, and digital signatures. <br />
Bitcoin and other cryptocurrencies use the private key and public key for digital signatures and validating transactions.<br />
 </br>
**Private key:**  </br>
The private key is just a big and random number. </br>
To generate a secure private key, you can use this [random entropy creator](https://github.com/tokimay/random_entropy).
 </br>
 </br>
**Public key:**  </br>
The public key is a coordinate calculated on the curve algorithm based on the private key.  </br>
To calculate public key, you can use [this source](https://github.com/tokimay/secp256k1_BTC_curve).


**Signing:**
````text
r, s = signature = ECDSA.sign(message, privateKey)
````

**Verify:**
````text
isVerify = ECDSA.verify(signature, message, publicKey)
````

**Example:**
````python
import secp256k1
import ECDSA

message = "Hello cryptography"
privateKey = 0x636678001c32339343b4ffadf02d1818e8a545926eebfdcf01f2b0f8573575c4
publicKey = secp256k1.compressed_public_key(privateKey)

r, s = signature = ECDSA.sign(message, privateKey)
print(f"r = {r}")
print(f"s = {s}")
print(f"Is verified? {ECDSA.verify(signature, message, publicKey)}")
````

**Result:**
````text
r = 92673285467210538520759924349025872011308897174686124168116777478326011855482
s = 14497835072239106761469671543678160546186472716622655380596629604178855582796
Is verified? True

Process finished with exit code 0
````