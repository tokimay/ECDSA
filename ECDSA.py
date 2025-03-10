
# This file is part of https://github.com/tokimay/ECDSA
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/ECDSA

import random
import SHA256
import secp256k1


def sign(message: str, private_key: str or int, r_helper: int = 0) -> tuple[int, int]:
    private_key = secp256k1.normalize(private_key)

    p = private_key
    h = int((SHA256.do_hash(message)), 16)
    # random number k
    k = h + p + r_helper
    # random point on curve
    r = secp256k1.multipy(repeat=k, point=secp256k1.g())
    # r = rx mod p
    r = r[0] % secp256k1.n()
    if r == 0:
        return sign(message, private_key, r_helper=random.randint(1, secp256k1.n()))
    k_inv = pow(k, -1, secp256k1.n())
    s = k_inv * (h + r * p) % secp256k1.n()
    return r, s


def verify(signature: tuple, message: str, public_key: tuple[int, int] or str or int) -> bool:
    if isinstance(public_key, tuple):
        pass
    elif isinstance(public_key, str) or isinstance(public_key, int):
        public_key = secp256k1.recover_public_key_coordinate(public_key)
    else:
        raise TypeError
    (r, s) = signature
    h = int((SHA256.do_hash(message)), 16)
    s_inv = pow(s, -1, secp256k1.n())
    # c = ((h * s_inverse) * G) + ((r * s_inverse) * publicKey)
    u = h * s_inv % secp256k1.n()
    v = r * s_inv % secp256k1.n()
    p1 = secp256k1.multipy(repeat=v, point=public_key)
    p2 = secp256k1.multipy(repeat=u, point=secp256k1.g())
    c = secp256k1.add(p1, p2)
    return c[0] == r
