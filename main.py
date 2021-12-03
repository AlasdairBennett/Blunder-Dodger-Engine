import time
from NegMaxx import NegMaxx

if __name__ == '__main__':
    testFen = "r6r/1b2k1bq/8/8/7B/8/8/R3K2R b KQ - 3 2"

    n = NegMaxx(testFen)

    start = time.time()
    print(n.nega_wrapper())
    end = time.time()
    print(end - start)
