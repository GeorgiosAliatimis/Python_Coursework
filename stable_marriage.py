import random
from collections.abc import Sequence
from tabulate import tabulate
from typing import TypeVar, Generic, Type, Dict, List, Sequence, Any

Sym: Any = int | str
Table = Dict[Sym,Sequence[Sym]]
class Stable_Marriage:
    def __init__(self, table_men: Table | None = None, 
                       table_women: Table | None = None,
                       n: int = 5, 
                       random_seed: int = 1) -> None:
        assert self.validate_table(table_men), 'Value of table_men is not valid'
        assert self.validate_table(table_women), 'Value of table_women is not valid'
        assert self.validate_tables_dimension(table_men,table_women), \
            'Values of table_men and table_women are valid, but they do not have the same dimensions.'
        assert self.validate_tables_share_symbols(table_men,table_women), \
            'Values of table_men and table_women are valid and have the same dimension, but use different symbols'
        self._symbols1: List[Sym]
        self._symbols2: List[Sym]
        self._table_men: Table
        self._table_women: Table
        if table_men is None or table_women is None:
            print("Arguments table_men or table_women not specified")
            self._symbols1 = list(range(n))
            self._symbols2 = list(range(n))
            random.seed(random_seed)
            self.generate_random_tables()
            print(f"Generated random tables for {n} men and {n} women.")
        else: 
            self._symbols1 = list(table_men.keys())
            self._symbols2 = list(table_women.keys())
            self._table_men = table_men 
            self._table_women = table_women
        self._rank_women: Dict[Sym,Dict[Sym,int]] = self.get_ranking(self._table_men)
        self._rank_men: Dict[Sym,Dict[Sym,int]] = self.get_ranking(self._table_women)

    def get_ranking(self,table: Table) -> Dict[Sym,Dict[Sym,int]]: 
        return {row: {v:i for i,v in enumerate(val)} for row,val in table.items()}

    def generate_random_tables(self):
        n : int = len(self._table_men)
        self._table_men = [ random.sample(range(n) ,n) for _ in range(n)] 
        self._table_women = [ random.sample(range(n) ,n) for _ in range(n)] 

    def validate_tables_dimension(self,table_men: Table|None, table_women: Table|None) -> bool:
        if table_men is None or table_women is None:    return True
        return len(table_men) == len(table_women)

    def validate_tables_share_symbols(self,table_men: Table|None, table_women: Table|None) -> bool:
        if table_men is None or table_women is None:    return True
        vals2_in_keys1: bool  =  all( all(y in table_men.keys()  for y in x) for x in table_women.values() )
        vals1_in_keys2: bool  =  all( all(y in table_women.keys()  for y in x) for x in table_men.values() )
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

    def matching_is_stable(self, matching: Dict[Sym,Sym]) -> int:
        for woman, men in self._table_women.items():
            for man in men:
                if man == matching[woman]:  continue
                curr_wife: Sym = matching[man]
                if self._rank_women[man][woman] < self._rank_women[man][curr_wife]:   
                    return False
        return True

    def scores(self, matching: Dict[Sym,Sym]) -> list[int]:
        score_men: int 
        score_women: int 
        score_men = sum(self._rank_women[man][matching[man]] for man in self._table_men)
        inv_matching: Dict[Sym,Sym] 
        score_women = sum(self._table_women[matching[man]].index(man) for man in self._table_men)
        return score_men, score_women

    def print_tables(self) -> None:
        n: int = len(self._table_men)
        for t in (self._table_men,self._table_women):
            matrix: List[List[Sym]] = [[k] + list(v) for k, v in t.items()]
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            headers: List[str] = [""] + [ordinal(i) for i in range(1,n+1)]
            print(tabulate( matrix,tablefmt="fancy_grid",headers=headers))

    def solve_problem(self,table_men: Table,table_women: Table):
        pass


if __name__ == "__main__":
    table_men: Table = dict()
    table_men["A"] = ["c","b","d","a"]
    table_men["B"] = ["b","a","c","d"]
    table_men["C"] = ["b","d","a","c"]
    table_men["D"] = ["c","a","d","b"]

    table_women: Table = dict()
    table_women["a"] = ["A","B","D","C"]
    table_women["b"] = ["C","A","D","B"]
    table_women["c"] = ["C","B","D","A"]
    table_women["d"] = ["B","A","C","D"]

    s: Stable_Marriage = Stable_Marriage(table_men,table_women)
    s.solve_problem(table_men,table_women)
    s.print_tables()
    print(s.get_ranking(s._table_men))
    print(s.get_ranking(s._table_women))
    matching: Dict[Sym,Sym] = dict()
    matching["A"] = "d"
    matching["B"] = "a"
    matching["C"] = "b"
    matching["D"] = "c"
    print(s.matching_is_stable(matching))