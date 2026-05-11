import random

def losuj_macierz(n: int) -> list[list[int]]:
    return [
        [0 if i == j else random.randint(1, 9000)
         for j in range(n)]
        for i in range(n)
    ]

def evaluate(permutacja):
    suma = 0
    for i in range(len(permutacja) - 1):
        for j in range(i + 1, len(permutacja)):
            suma += macierz[permutacja[i]][permutacja[j]]
    return (suma,)

N = 10  # długość permutacji
macierz = losuj_macierz(N)
