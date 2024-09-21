import random

def compare_strs(a, b, max_spaces, space_char, space_chance):
    add_space = []
    space_count = b.count(space_char)
    for n in range(min([len(a), len(b)])):
         if a[n] != b[n]:
            add_space.append(n)
         if (len(add_space) + space_count) > max_spaces: return False, []
    if len(add_space) == 1: return True, add_space
    result = [space for space in add_space if random.random() < space_chance]
    return True, result

class Compression:
    def __init__(self, max_spaces: int = 1, space_char = chr(0), space_chance: float = 0.2):
        self.patterns = []
        self.max_spaces = max_spaces
        self.space_char = space_char
        self.space_chance = space_chance
    def add_pattern(self, pattern):
        if len(pattern) < 2: raise TypeError(f"Pattern to add can't be length {len(pattern)}. It is '{pattern}'.")
        not_found = True
        for n, p in enumerate(self.patterns):
            comparison = compare_strs(p[0], pattern, self.max_spaces, self.space_char, self.space_chance)
            if comparison[0]:
                self.patterns[n] = (p[0], p[1]+1)
                not_found = len(comparison[1]) != 0
                for char_num in comparison[1]:
                    t = list(self.patterns[n][0])
                    t[char_num] = self.space_char
                    t = ''.join(t)
                    self.patterns[n] = (t, self.patterns[n][1])
                break
        if not_found:
            self.patterns.append((pattern, 0))
        for n, p in enumerate(self.patterns[:-1]):
            if p[1] < self.patterns[n+1][1]:
                t = p[1]
                self.patterns[n] = self.patterns[n+1]
                self.patterns[n+1] = t
    def __call__(self, data):
        self.add_pattern(data)
        print(self.patterns)

if __name__ == "__main__":
    compression = Compression()

    while True:
        data = input("Data: ")
        compression(data)
