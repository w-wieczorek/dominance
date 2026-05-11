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
