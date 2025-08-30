def kmp_table(pattern):
    """Constructs the partial match table for KMP algorithm."""
    table = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        if pattern[i] == pattern[j]:
            j += 1
            table[i] = j
        else:
            j = table[j - 1]
            while j > 0 and pattern[i] != pattern[j]:
                j = table[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            table[i] = j
    return table


def kmp_search(text, pattern):
    """Performs KMP string matching algorithm."""
    table = kmp_table(pattern)
    matches = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = table[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)  # match found
            j = table[j - 1]
    return matches


# Example usage:
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
matches = kmp_search(text, pattern)

# Output the result
print(f"The pattern was found at indices: {matches}")
