import math

def add_pattern(data, pattern):
    text = list(data)
    for n, c in enumerate(pattern):
        if c == "\x00": continue
        if n >= len(text):
            text.append(c)
        else:
            text[n] = c
    return ''.join(text)

def match_in(match, text):
    return any(p == c for p, c in zip(match, text))

class Patterns:
    def __init__(self):
        self.patterns = []

    def __call__(self, s):
        matches = []
        len_s = len(s)
        result = ""

        # Compare the string with the existing patterns
        for i, pattern in enumerate(self.patterns):
            r = add_pattern(result, pattern)
#                if s == "а..": print(math.fsum(p == c for p, c in zip(r, s)), math.fsum(p == c for p, c in zip(result, s)), result, r, i)
            r = r[:len_s]
            result = result[:len_s]
            if r != result and (math.fsum(p == c for p, c in zip(r, s)) > math.fsum(p == c for p, c in zip(result, s))):
                matches.append(i)
                result = r

        # If no matches, create or merge a new pattern
        if result != s:
            new_pattern = self._combine_patterns(s)
            # Avoid adding duplicate patterns
            if new_pattern not in self.patterns:
                matches.append(len(self.patterns))
                self.patterns.append(new_pattern)
            else:
                matches.append(self.patterns.index(new_pattern))
        result_matches = []
        for n in range(len(matches)):
            t = matches.copy()
            t.pop(n)
            if self.reconstruct(t)[:len_s] != result:
                result_matches.append(matches[n])
        return result_matches
    
    def reconstruct(self, ptrns):
        result = ""
        for ptrn in ptrns:
            result = add_pattern(result, self.patterns[ptrn])
        return result.replace('\x00', " ")

    def _combine_patterns(self, s):
        # Start with the new string as the base
        new_pattern = list(s)
        len_s = len(s)

        # Compare with existing patterns and combine them
        for pattern in self.patterns:
            for i in range(min([len_s, len(pattern)])):
                if pattern[i] != new_pattern[i]:
                    new_pattern[i] = '\x00'  # Mark the differences
                if new_pattern.count('\x00') >= len(new_pattern): new_pattern = list(s)

        return ''.join(new_pattern)

if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt
    from tqdm import tqdm
    
    def get_dataset():
        with open("dataset.txt", "r") as file:
            for line in tqdm(file.read().split('\n')[:1000]):
                ls = line.strip()
                if len(ls) > 1:
                    yield line.lower()
    
    compression = Patterns()

    plot = []
    accuracy_list = []

    for data in get_dataset():
        res = compression(data)
        reconstruction = compression.reconstruct(res)
        len_data = len(data)
        eff = len(res)/len_data
        plot.append(eff)
        accuracy = math.fsum([a==b for a, b in zip(data, reconstruction)])/len_data
        accuracy_list.append(accuracy)
    plot_arr = np.array([plot, accuracy_list])
    print("Average compression precentage:", np.average(plot_arr[0]))
    plot_arr = plot_arr.T
    plt.plot(plot_arr)
    plt.show()
    plot = []
    accuracy_list = []
    while True:
        data = input("Text: ")
        res = compression(data)
        print(res)
        reconstruction = compression.reconstruct(res)
        print(reconstruction)
        len_data = len(data)
        eff = len(res)/len_data
        accuracy = math.fsum([a==b for a, b in zip(data, reconstruction)])/len_data
        accuracy_list.append(accuracy)
        print('Accuracy:', accuracy)
        print('Compression:', eff)
        plot.append(eff)
        if len(plot) % 20 == 0:
            plot_arr = np.array([plot, accuracy_list])
            print("Average compression precentage:", np.average(plot_arr[0]))
            plot_arr = plot_arr.T
            plt.plot(plot_arr)
            plt.show()

