import numpy as np

def test():
    A = np.arange(12, dtype=float).reshape(1,1,2,6)
    B = np.transpose(A, axes=(0,1,3,2))
    print(B)

if __name__ == "__main__":
    test()