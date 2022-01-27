from stable_marriage import Stable_Marriage_Random_Tables
import matplotlib.pyplot as plt
import random
from numpy import transpose, linspace

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
# plot_hist(10)
# plot_hist(100,M=300)

n_vals =  2**linspace(1,10,10)
scores_men = [None] * len(n_vals)
scores_women = [None] * len(n_vals)
for i, n in enumerate(n_vals):
    scores_men[i], scores_women[i] = random_scores(int(n),M=50)

n_vals_str = [str(int(num)) for num in n_vals]
ax = plt.subplot()
for score,c in  [(scores_men,"blue"), (scores_women,"red")]:
    ax.boxplot(transpose(score), boxprops=dict(color=c),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                positions = n_vals,
                widths= n_vals/3
                )
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel(r'n')
ax.set_title('Score whisker plots')
plt.savefig("scores_whisker_plot.png")