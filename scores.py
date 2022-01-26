from stable_marriage import Stable_Marriage_Random_Tables
import matplotlib.pyplot as plt
import random

def random_scores(n):
    r = Stable_Marriage_Random_Tables(n)
    match = r.solve_problem()
    return r.compute_score(match)

M = 1000 
scores_men = [None] * M
scores_women = [None] * M
random.seed(1)
for i in range(M):
    scores_men[i], scores_women[i] = random_scores(n=10)
plt.hist(scores_men)
plt.hist(scores_women)
plt.show()