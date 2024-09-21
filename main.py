import random


def compare_strs(str_a, str_b, space_limit, space_char, padding_char, space_chance):
    add_space = []
    space_count = str_b.count(space_char)
    len_a, len_b = len(str_a), len(str_b)
    l = max([len_a, len_b])
    minl = min([len_a, len_b])
    a = str_a+padding_char*(l-len_a)
    b = str_b+padding_char*(l-len_b)
    for n in range(minl):
         if a[n] != b[n]:
            add_space.append(n)
         if (len(add_space) + space_count) > (l-space_limit): return False, []
    if len(add_space) == 1: return True, add_space
    result = [space for space in add_space if (random.random() < space_chance) and space < minl]
    return True, result


class Compression:
    def __init__(self, space_limit: int = 1, space_char = chr(0), padding_char = chr(1), space_chance: float = 0.2):
        self.patterns = []
        self.space_limit = space_limit
        self.space_char = space_char
        self.padding_char = padding_char
        self.space_chance = space_chance
    def add_pattern(self, pattern):
        if len(pattern) < 2: raise TypeError(f"Pattern to add can't be length {len(pattern)}. It is '{pattern}'.")
        not_found = True
        for n, p in enumerate(self.patterns):
            comparison = compare_strs(p[0], pattern, self.space_limit, self.space_char, self.padding_char, self.space_chance)
            if comparison[0]:
                self.patterns[n] = (p[0], p[1]+1)
                not_found = len(comparison[1]) != 0
                for char_num in comparison[1]:
                    t = list(self.patterns[n][0])
                    t[char_num] = self.space_char
                    t = ''.join(t)
                    self.patterns[n] = (t, self.patterns[n][1])
        if not_found:
            self.patterns.append((pattern, 0))
        for n, p in enumerate(self.patterns[:-1]):
            if p[1] < self.patterns[n+1][1]:
                t = p[1]
                self.patterns[n] = self.patterns[n+1]
                self.patterns[n+1] = t
    def __call__(self, data):
        print(self.patterns)
        self.add_pattern(data)


if __name__ == "__main__":
    compression = Compression()

    while True:
        data = input("Data: ")
        compression(data)

