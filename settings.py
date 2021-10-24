ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_to_36(num):
    if num < 36:
        return ALPHABET[num]
    else:
        return convert_to_36(num // 36) + ALPHABET[num % 36]


def create_key(map):
    chain = []
    for lay in map:
        block = ''
        for place in lay:
            if place == 0:
                block += '0'
            else:
                block += '1'
        chain.append(convert_to_36(int(block, 2)))
    return ':'.join(chain)


def create_map(map):
    for n, layer in enumerate(map):
        for num, place in enumerate(layer):
            if n == 0 and num == 0:
                map[n][num] = 4
            else:
                pass
