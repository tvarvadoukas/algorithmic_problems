"""
Generate critics and novels they like.
"""
from random import randint, sample

N_CRITICS = (100000, 500000)
N_NOVELS = (4, 20)

if __name__ == "__main__":
    import sys
    max_critics, max_novels = N_CRITICS[1], N_NOVELS[1]
    min_critics, min_novels = N_CRITICS[0], N_NOVELS[0]

    if len(sys.argv) >= 2:
        max_critics = int(sys.argv[1])
    if len(sys.argv) >= 3:
        max_novels = int(sys.argv[2])

    c = randint(min_critics, max_critics)
    n = randint(min_novels, max_novels)
    novels = range(1, n+1)

    print "%d %d" % (c, n)
    for _ in xrange(c):
        k = randint(1, n)
        preferences = map(str, sample(novels, k))
        print "%s" % " ".join(preferences)
