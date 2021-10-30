from random import randrange

ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_to_36(num):
    if num < 36:
        return ALPHABET[num]
    else:
        return convert_to_36(num // 36) + ALPHABET[num % 36]


# конвертирует 10-ричную систему счисления в 36-ричную


def create_key(map):
    chain = [str(int(len(map[0]) ** 0.5))]
    for lay in map:
        block = ''
        for place in lay:
            if place.type == 'lava':
                block += '1'
            else:
                block += '0'
        chain.append(convert_to_36(int(block, 2)))
    return ':'.join(chain)


# создает ключ генерации принимая карту

def create_map_by_key(self, key):
    lenth = int(key[:1]) ** 2
    key = key[2:]
    self.map = []
    for cnt, l in enumerate(key.split(':')):  # l = layer
        l = str(bin(int(l, 36)))[2:]
        while lenth != len(l):
            l = '0' + l
        layer = []
        print(l)
        for n, c in enumerate(list(l)):  # c = cell
            if cnt == 0 and n == 0:
                layer.append(Cell('ship', player=True))
            elif c == '1':
                layer.append(Cell('lava'))
            else:
                layer.append(Cell('ground'))
        self.map.append(layer)



class Cell:
    def __init__(self, type, up_way=False, down_way=False, player=False):
        self.type = type
        self.up_way = up_way
        self.down_way = down_way
        self.player = player
# класс для каждой клетки
