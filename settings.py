ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_to_36(num):
    if num < 36:
        return ALPHABET[num]
    else:
        return convert_to_36(num // 36) + ALPHABET[num % 36]


# конвертирует 10-ричную систему счисления в 36-ричную


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


# создает ключь генерации принимая карту

class Cell:
    def __init__(self, type, up_way=False, down_way=False):
        self.type = type
        self.up_way = up_way
        self.down_way = down_way
