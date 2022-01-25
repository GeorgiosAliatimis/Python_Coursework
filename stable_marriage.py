import random
from collections import deque
from tabulate import tabulate
from typing import TypeVar, Generic, Type, Dict, List, Sequence 

Sym = int | str
Table = Dict[Sym,Sequence[Sym]]
class Stable_Marriage:
    def __init__(self, table1: Table | None = None, 
                       table2: Table | None = None,
                       n: int = 5) -> None:
        assert self.validate_table(table1), 'Value of table1 is not valid'
        assert self.validate_table(table2), 'Value of table2 is not valid'
        assert self.validate_tables(table1,table2), \
            'Values of table1 and table2 are valid, but they do not have the same dimensions.'
        self._symbols1: List[Sym]
        self._symbols2: List[Sym]
        self._table1: List[List[int]]
        self._table2: List[List[int]]
        if table1 is None or table2 is None:
            print("Arguments table1 or table2 not specified")
            self._symbols1 = list(range(n))
            self._symbols2 = list(range(n))
            self.generate_random_tables()
            print(f"Generated random tables for {n} men and {n} women.")
        else: 
            self._symbols1 = list(table1.keys())
            self._symbols2 = list(table2.keys())
            self._table1 = table1 
            self._table2 = table2
            # self._table1 = [ 
            #     [self._symbols2.index(sym2)  for sym2 in table1[sym1]] 
            # for sym1 in self._symbols1]
            # self._table2 = [ 
            #     [self._symbols1.index(sym1)  for sym1 in table2[sym2]] 
            # for sym2 in self._symbols2]
            

    def generate_random_tables(self):
        pass 

    def validate_tables(self,table1: Table|None, table2: Table|None) -> bool:
        return True 

    def validate_table(self,table: Table | None) -> bool:
        return True

    def matching_is_stable(self,table1: Table,table2: Table,matching) -> int:
        pass

    def scores(self,table1: Table, table2: Table, matching) -> list[int]:
        pass 

    def print_tables(self) -> None:
        print(self._table1)
        print(self._table2)

    def solve_problem(self,table1: Table,table2: Table):
        # matching = dict()
        pass

table1: Table = dict()
table1["A"] = ["c","b","d","a"]
table1["B"] = ["b","a","c","d"]
table1["C"] = ["b","d","a","c"]
table1["D"] = ["c","a","d","b"]

table2: Table = dict()
table2["a"] = ["A","B","D","C"]
table2["b"] = ["C","A","D","B"]
table2["c"] = ["C","B","D","A"]
table2["d"] = ["B","A","C","D"]

s: Stable_Marriage = Stable_Marriage(table1,table2)
s.solve_problem(table1,table2)
s.print_tables()