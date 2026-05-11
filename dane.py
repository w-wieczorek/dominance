import random

def losuj_macierz(n: int) -> list[list[int]]:
    return [
        [0 if i == j else random.randint(0, 1)
         for j in range(n)]
        for i in range(n)
    ]

def evaluate(permutacja):
    suma = 0
    for i in range(len(permutacja) - 1):
        for j in range(i + 1, len(permutacja)):
            suma += macierz[permutacja[i]][permutacja[j]]
    return (suma,)

N = 12  # długość permutacji
macierz = losuj_macierz(N)
for i in range(N - 1):
    for j in range(i + 1, N):
        macierz[j][i] = 1 - macierz[i][j]

