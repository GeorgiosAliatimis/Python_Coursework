from stable_marriage import Stable_Marriage, Stable_Marriage_Random_Tables
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from numpy import log, exp

def average_execution_time(fun,M=1000,silent=False):
    start = time.perf_counter()
    for _ in range(M): fun()
    end = time.perf_counter()   
    aet = (end-start)/M
    if silent:  return aet
    print(f"Average time of execution for {fun.__name__} is {aet} seconds")

def given_example():
    table_men = {'A': ['c', 'b', 'd', 'a'], 'B': ['b', 'a', 'c', 'd'], \
        'C': ['b', 'd', 'a', 'c'], 'D': ['c', 'a', 'd', 'b']}
    table_women = {'a': ['A', 'B', 'D', 'C'], 'b': ['C', 'A', 'D', 'B'], \
        'c': ['C', 'B', 'D', 'A'], 'd': ['B', 'A', 'C', 'D']}
    s = Stable_Marriage(table_men,table_women)
    s.solve_problem()

average_execution_time(given_example)

def random_example(n):
    r = Stable_Marriage_Random_Tables(n)
    r.solve_problem()

n_vals = list(range(5,101))
aets = list()
for n in n_vals:
    fun = lambda : random_example(n)
    fun.__name__ = f"random_example_n={n}"
    aets.append(average_execution_time(fun,M=20,silent=True))

model = LinearRegression().fit( log(n_vals).reshape((-1, 1)) ,  log(aets) )
print(f"The coefficient of linear regression is {model.coef_}")
plt.loglog(n_vals,aets)
plt.loglog(n_vals, exp(model.intercept_) * n_vals**model.coef_,\
    color='black', linestyle='dashed')
plt.xlabel(r"n")
plt.title("Execution time of Stable Marriage")
plt.legend(["Execution time","Fitted"])
# plt.savefig("execution_time.png",format="png")
plt.show()