from multiprocessing import Process, Array, Pool


def f(X, a, b):
    X[a][b] = a + b


if __name__ == "__main__":
    X = [Array("i", [0, 0, 0])for i in range(100)]
    for i in range(100):
        for j in range(3):
            p = Process(target=f, args=(X, i, j))
            p.start()
            p.join()
    print([X[i][:]for i in range(100)])
