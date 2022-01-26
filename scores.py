from stable_marriage import Stable_Marriage_Random_Tables
import matplotlib.pyplot as plt
import random

def random_score(n):
    r = Stable_Marriage_Random_Tables(n)
    match = r.solve_problem()
    return r.compute_score(match)

def random_scores(n, M= 1000):
    scores_men = [None] * M
    scores_women = [None] * M
    for i in range(M):
        scores_men[i], scores_women[i] = random_score(n)
    return scores_men, scores_women

def plot_hist(n, **kwargs):
    scores_men, scores_women = random_scores(n,**kwargs)
    plt.hist(scores_men, alpha=0.8)
    plt.hist(scores_women, alpha=0.8)
    plt.xlabel("Score")
    plt.title(f"Scores for n={n}")
    plt.legend(["Proposer","Acceptor"])
    plt.savefig(f"scores_n={n}.png",format="png")

random.seed(1)
plot_hist(10)
plot_hist(100,M=300)