import dane
import ga
import sys
# import heapq

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
    def generate_children(self):
        for i in range(dane.N):
            if i not in self.perm:
                child = PartialSolution()
                child.perm = self.perm + [i]
                child.compute_bound()
                yield child
    
best = ga.mainAG()
best_value = dane.evaluate(best)[0]
Z = []
start_point = PartialSolution()
start_point.compute_bound()
# heapq.heappush(Z, (-start_point.bound, start_point))
Z.append((-start_point.bound, start_point))  # Dodajemy początkowy węzeł do kolejki
while Z:
    # bound, node = heapq.heappop(Z)
    bound, node = Z.pop() 
    bound = -bound
    if bound <= best_value:
        continue
    if node.is_complete():
        if bound > best_value:
            best_value = bound
            print("Nowa najlepsza wartość:", best_value)
            best = node.perm
    else:
        for child in node.generate_children():
            if child.bound > best_value:
                # heapq.heappush(Z, (-child.bound, child))
                Z.append((-child.bound, child))
print("Najlepsza permutacja:", best)
print("Najlepsza wartość:", best_value)

p = 0
psi = [-1] * dane.N
psi[0] = 0
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
            current_step = 10
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
        if dane.macierz[psi[p-1]][psi[p]] >= dane.macierz[psi[p]][psi[p-1]]:
            current_step = 9
        else:
            current_step = 2
    elif n == 9:
        psol = PartialSolution()
        psol.perm = psi[:p+1]
        psol.compute_bound()
        if psol.bound > fL:
            current_step = 1
        else:
            current_step = 2
    elif n == 10:
        psi[p] = -1
        p -= 1
        current_step = 2

while True:
    step(current_step)

