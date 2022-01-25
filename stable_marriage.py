import random
from collections.abc import Sequence
from tabulate import tabulate
from typing import TypeVar, Generic, Type, Dict, List, Sequence, Any

Sym: Any = int | str
Table = Dict[Sym,Sequence[Sym]]
class Stable_Marriage:
    def __init__(self, table1: Table | None = None, 
                       table2: Table | None = None,
                       n: int = 5, 
                       random_seed: int = 1) -> None:
        assert self.validate_table(table1), 'Value of table1 is not valid'
        assert self.validate_table(table2), 'Value of table2 is not valid'
        assert self.validate_tables_dimension(table1,table2), \
            'Values of table1 and table2 are valid, but they do not have the same dimensions.'
        assert self.validate_tables_share_symbols(table1,table2), \
            'Values of table1 and table2 are valid and have the same dimension, but use different symbols'
        self._symbols1: List[Sym]
        self._symbols2: List[Sym]
        self._table1: Table
        self._table2: Table
        if table1 is None or table2 is None:
            print("Arguments table1 or table2 not specified")
            self._symbols1 = list(range(n))
            self._symbols2 = list(range(n))
            random.seed(random_seed)
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
        n : int = len(self._table1)
        self._table1 = [ random.sample(range(n) ,n ) for _ in range(n)] 
        self._table2 = [ random.sample(range(n) ,n ) for _ in range(n)] 

    def validate_tables_dimension(self,table1: Table|None, table2: Table|None) -> bool:
        if table1 is None or table2 is None:    return True
        return len(table1) == len(table2)

    def validate_tables_share_symbols(self,table1: Table|None, table2: Table|None) -> bool:
        if table1 is None or table2 is None:    return True
        vals2_in_keys1: bool  =  all( all(y in table1.keys()  for y in x) for x in table2.values() )
        vals1_in_keys2: bool  =  all( all(y in table2.keys()  for y in x) for x in table1.values() )
        return vals1_in_keys2 and vals2_in_keys1

    def validate_table(self,table: Table | None) -> bool:
        if table is None:   return True
        is_right_type: bool=isinstance(table,dict) and  \
                            all(isinstance(x, Sequence) for x in table.values()) and \
                            all(all(isinstance(y, Sym.__args__) for y in x) for x in table.values())  
        if not is_right_type:   return False
        n: int = len(table[next(iter(table))])
        has_consistent_dimension: bool = all(len(x) == n for x in table.values())
        if not has_consistent_dimension: return False
        return True

    def matching_is_stable(self,table1: Table,table2: Table,matching) -> int:
        pass

    def scores(self,table1: Table, table2: Table, matching) -> list[int]:
        pass 

    def print_tables(self) -> None:
        n: int = len(self._table1)
        for t in (self._table1,self._table2):
            matrix: List[List[Sym]] = [[k] + list(v) for k, v in t.items()]
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            headers: List[str] = [""] + [ordinal(i) for i in range(1,n+1)]
            print(tabulate( matrix,tablefmt="fancy_grid",headers=headers))

    def solve_problem(self,table1: Table,table2: Table):
        pass


if __name__ == "__main__":
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