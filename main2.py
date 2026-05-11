import dane
import ga
import sys

class PartialSolution(object):
    def __init__(self):
        self.perm = []
        self.bound = -1
    def is_complete(self):
        return len(self.perm) == dane.N
    def __lt__(self, other):
        return self.bound > other.bound  # Odwrócona kolejność dla max-heap
    def compute_bound(self):
        self.bound = 0
        used = set()
        for i in range(len(self.perm) - 1):
            for j in range(i + 1, len(self.perm)):
                self.bound += dane.macierz[self.perm[i]][self.perm[j]]
                if self.perm[i] < self.perm[j]:
                    used.add((self.perm[i], self.perm[j]))
                else:
                    used.add((self.perm[j], self.perm[i]))
        for i in range(dane.N - 1):
            for j in range(i + 1, dane.N):
                if (i, j) not in used:
                    self.bound += max(dane.macierz[i][j], dane.macierz[j][i])

p = 0
psi = list(range(dane.N))
best = ga.mainAG()
fL = dane.evaluate(best)[0]
current_step = 1
brakujacy = list(range(dane.N))

def step(n):
    global p, psi, best, fL, current_step, brakujacy
    if n == 1:
        p += 1
        current_step = 2
    elif n == 2:
        psi[p] = psi[p] + 1
        current_step = 3
    elif n == 3:
        if any(psi[p] == psi[k] for k in range(p)):
            current_step = 2
        else:
            current_step = 4
    elif n == 4:
        if p == 0 and psi[p] > dane.N - 1:
            print("Najlepsza permutacja:", best)
            print("Najlepsza wartość:", fL)
            sys.exit(0)
        else:
            current_step = 5
    elif n == 5:
        if p > 0 and psi[p] > dane.N - 1:
            current_step = 9
        else:
            current_step = 6
    elif n == 6:
        if p == dane.N - 2:
            for i in range(dane.N):
                brakujacy[i] = 0
            for i in range(dane.N - 1):
                brakujacy[psi[i]] = 1
            for i in range(dane.N):
                if brakujacy[i] == 0:
                    psi[dane.N - 1] = i
                    break
            current_step = 7
        else:
            current_step = 8
    elif n == 7:
        f = dane.evaluate(psi)[0]
        if f > fL:
            best = psi.copy()
            fL = f
            print("Nowa najlepsza wartość:", fL)
        current_step = 2
    elif n == 8:
        psol = PartialSolution()
        psol.perm = psi
        psol.compute_bound()
        if psol.bound > fL:
            current_step = 1
        else:
            current_step = 2
    elif n == 9:
        psi[p] = -1
        p -= 1
        current_step = 2

while True:
    step(current_step)
