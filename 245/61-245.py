def shortest_dist(l, word_1, word_2):
    min_dist = None

    if word_1 == word_2:
        first = None
        for i, w in enumerate(l):
            if w == word_1:
                if first is not None:
                    d = i - first
                    min_dist = d if min_dist is None else min(min_dist, d)
                first = i
        return min_dist

    left, right = None, None
    for i, w in enumerate(l):
        if w == word_1:
            left = i
            if right is not None:
                d = i - right
                min_dist = d if min_dist is None else min(min_dist, d)
        elif w == word_2:
            right = i
            if left is not None:
                d = i - left
                min_dist = d if min_dist is None else min(min_dist, d)
    return min_dist


print(shortest_dist(["a", "d", "v", "k", "b", "a", "a", "b", "a", "e", "e"], "a", "a"))
print(shortest_dist(["e", "e"], "e", "e"))
print(shortest_dist(["e", "a", "e"], "e", "e"))
print(shortest_dist(["a", "b", "e", "e"], "a", "e"))
print(shortest_dist(["a", "e", "e", "b"], "a", "b"))
print(shortest_dist(["a", "e", "b", "d", "b"], "a", "b"))
print(shortest_dist(["a", "e", "a", "b", "b"], "a", "b"))