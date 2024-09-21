class Patterns:
    def __init__(self):
        self.patterns = []

    def __call__(self, s):
        matches = []

        # Compare the string with the existing patterns
        for i, pattern in enumerate(self.patterns):
            if len(pattern) == len(s) and all(p == c or p == '\x00' for p, c in zip(pattern, s)):
                matches.append(i)

        # If no matches, create or merge a new pattern
        if not matches:
            new_pattern = self._combine_patterns(s)
            # Avoid adding duplicate patterns
            if new_pattern not in self.patterns:
                self.patterns.append(new_pattern)
                matches.append(len(self.patterns) - 1)
            else:
                matches.append(self.patterns.index(new_pattern))

        return matches

    def _combine_patterns(self, s):
        # Start with the new string as the base
        new_pattern = list(s)

        # Compare with existing patterns and combine them
        for pattern in self.patterns:
            if len(pattern) == len(s):
                for i in range(len(s)):
                    if pattern[i] != new_pattern[i]:
                        new_pattern[i] = '\x00'  # Mark the differences
                    if new_pattern.count('\x00') >= len(new_pattern)-1: new_pattern = list(s)

        return ''.join(new_pattern)

if __name__ == "__main__":
    patterns = Patterns()

    while True:
        data = input("Data: ")
        print(patterns(data))
        print(patterns.patterns)

