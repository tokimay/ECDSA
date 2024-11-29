
def _right_rotate(number: int, rotations: int) -> int:
    return (2 ** 32 - 1) & (number >> rotations | number << (32 - rotations))


def _right_shift(number: int, shift: int) -> int:
    return number >> shift


def _xor(number1: int, number2: int) -> int:
    return number1 ^ number2


def _and(number1: int, number2: int) -> int:
    return number1 & number2


def _not(number):
    return ~number


def _is_hex(_input: str) -> bool:
    try:
        int(_input, 16)
        return True
    except ValueError:
        return False

def do_hash(_input: str or bytes or int or bytearray) -> str:
    a = h0 = 1779033703
    b = h1 = 3144134277
    c = h2 = 1013904242
    d = h3 = 2773480762
    e = h4 = 1359893119
    f = h5 = 2600822924
    g = h6 = 528734635
    h = h7 = 1541459225

    k = [
        1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221,
        3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580,
        3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986,
        2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895,
        666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037,
        2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344,
        430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779,
        1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298
    ]

    if isinstance(_input, str):
        if _is_hex(_input):
            bytearray_input = bytearray.fromhex(_input)
        else:
            bytearray_input = bytearray(_input, 'UTF-8')
    elif isinstance(_input, bytes):
        bytearray_input = bytearray(_input)
    elif isinstance(_input, int):
        message = _input.to_bytes((_input.bit_length() + 7) // 8, 'big')
        bytearray_input = bytearray(message)
    elif isinstance(_input, bytearray):
        bytearray_input = _input
    else:
        raise TypeError

    length_bytearray_input = len(bytearray_input) * 8
    bytearray_input.append(0x80)

    while ((len(bytearray_input) * 8 + 64) % 512) != 0:
        bytearray_input.append(0x00)

    bytearray_input += length_bytearray_input.to_bytes(8, 'big')

    # check if the padding complete

    chunks = []
    for i in range(0, len(bytearray_input), 64):
        chunks.append(bytearray_input[i:i + 64])

    for chunk in chunks:
        bytearray_input_schedule = []
        for i in range(0, 64 * 4, 4):
            bytearray_input_schedule.append(chunk[i:i + 4])
        for i in range(0, 48, 1):
            term1 = int(bytearray_input_schedule[i].hex(), 16)
            term2 = int(bytearray_input_schedule[i + 1].hex(), 16)
            term3 = int(bytearray_input_schedule[i + 9].hex(), 16)
            term4 = int(bytearray_input_schedule[i + 14].hex(), 16)

            term1_rr_7 = _right_rotate(term2, 7)
            term1_rr_18 = _right_rotate(term2, 18)
            term1_rs_3 = _right_shift(term2, 3)
            term1_xor = _xor(_xor(term1_rr_7, term1_rr_18), term1_rs_3)

            term4_rr_17 = _right_rotate(term4, 17)
            term4_rr_19 = _right_rotate(term4, 19)
            term4_rs_10 = _right_shift(term4, 10)
            term4_xor = _xor(_xor(term4_rr_17, term4_rr_19), term4_rs_10)

            result = ((term1 + term1_xor + term3 + term4_xor) % 2 ** 32)
            bytearray_input_schedule[i + 16] = result.to_bytes(8, 'big')
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for i in range(0, 64, 1):
            w = int(bytearray_input_schedule[i].hex(), 16)
            sigma0 = _xor(_xor(_right_rotate(a, 2), _right_rotate(a, 13)), _right_rotate(a, 22))
            sigma1 = _xor(_xor(_right_rotate(e, 6), _right_rotate(e, 11)), _right_rotate(e, 25))
            choice = _xor((_and(e, f)), (_and((_not(e)), g)))
            majority = _xor(_xor((_and(a, b)), (_and(a, c))), (_and(b, c)))
            temp2 = ((sigma0 + majority) % 2 ** 32)
            temp1 = (h + sigma1 + choice + k[i] + w) % 2 ** 32
            h = g
            g = f
            f = e
            e = (d + temp1) % 2 ** 32
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % 2 ** 32
        h0 = (h0 + a) % 2 ** 32
        h1 = (h1 + b) % 2 ** 32
        h2 = (h2 + c) % 2 ** 32
        h3 = (h3 + d) % 2 ** 32
        h4 = (h4 + e) % 2 ** 32
        h5 = (h5 + f) % 2 ** 32
        h6 = (h6 + g) % 2 ** 32
        h7 = (h7 + h) % 2 ** 32

    h0 = hex(h0)[2:].zfill(8)
    h1 = hex(h1)[2:].zfill(8)
    h2 = hex(h2)[2:].zfill(8)
    h3 = hex(h3)[2:].zfill(8)
    h4 = hex(h4)[2:].zfill(8)
    h5 = hex(h5)[2:].zfill(8)
    h6 = hex(h6)[2:].zfill(8)
    h7 = hex(h7)[2:].zfill(8)

    return h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
