import random
from collections.abc import Sequence
from tabulate import tabulate
from typing import Iterable, TypeVar, Generic, Type, Dict, List, Sequence, Any, Tuple

Sym: Any = int | str
Table = Dict[Sym,Sequence[Sym]]
class Stable_Marriage:
    def __init__(self, table_men: Table, 
                       table_women: Table) -> None:
        assert self.validate_table(table_men), 'Value of table_men is not valid'
        assert self.validate_table(table_women), 'Value of table_women is not valid'
        assert self.validate_tables_dimension(table_men,table_women), \
            'Values of table_men and table_women are valid, but they do not have the same dimensions.'
        assert self.validate_tables_share_symbols(table_men,table_women), \
            'Values of table_men and table_women are valid and have the same dimension, but use different symbols'
        self._table_men: Table   = table_men 
        self._table_women: Table = table_women
        self._rank_women: Dict[Sym,Dict[Sym|None,int]] = self.compute_ranking(self._table_men)
        self._rank_men: Dict[Sym,Dict[Sym|None,int]] = self.compute_ranking(self._table_women)

    def compute_ranking(self,table: Table) -> Dict[Sym,Dict[Sym|None,int]]: 
        return {key: {v:i for i,v in enumerate(val)} | {None:len(val)}  for key,val in table.items()}

    def validate_tables_dimension(self,table_men: Table, table_women: Table) -> bool:
        return len(table_men) == len(table_women)

    def validate_tables_share_symbols(self,table_men: Table, table_women: Table) -> bool:
        vals2_in_keys1: bool  =  all( all(y in table_men.keys()  for y in x) for x in table_women.values() )
        vals1_in_keys2: bool  =  all( all(y in table_women.keys()  for y in x) for x in table_men.values() )
        return vals1_in_keys2 and vals2_in_keys1

    def validate_table(self,table: Table) -> bool:
        is_right_type: bool=isinstance(table,dict) and  \
                            all(isinstance(x, Sequence) for x in table.values()) and \
                            all(all(isinstance(y, Sym.__args__) for y in x) for x in table.values())  
        if not is_right_type:   return False
        n: int = len(table[next(iter(table))])
        has_consistent_dimension: bool = all(len(x) == n for x in table.values())
        if not has_consistent_dimension: return False
        return True

    def matching_is_stable(self, matching: Dict[Sym,Sym]) -> int:
        woman: Sym
        man: Sym 
        men: Iterable[Sym] 
        for woman, men in self._table_women.items():
            for man in men:
                if woman == matching[man]:  break
                curr_wife: Sym = matching[man]
                if self._rank_women[man][woman] < self._rank_women[man][curr_wife]:   
                    return False
        return True

    def compute_score(self, matching: Dict[Sym,Sym]) -> Tuple[int,int]:
        score_men: int 
        score_women: int 
        score_men = sum(self._rank_women[man][matching[man]] for man in self._table_men)
        score_women = sum(self._table_women[matching[man]].index(man) for man in self._table_men)
        return score_men, score_women

    def print_tables(self) -> None:
        n: int = len(self._table_men)
        t: Table
        for t in (self._table_men,self._table_women):
            matrix: List[List[Sym]] = [[k] + list(v) for k, v in t.items()]
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            headers: List[str] = [""] + [ordinal(i) for i in range(1,n+1)]
            print(tabulate( matrix,tablefmt="fancy_grid",headers=headers))

    def solve_problem(self) -> Dict[Sym,Sym]:
        man_individual_score: Dict[Sym,int] = {man:0 for man in self._table_men}
        matching: Dict[Sym,Sym|None] = {man: None for man in self._table_men}
        inv_matching: Dict[Sym,Sym|None] = {woman: None for woman in self._table_women}
        man: Sym|None
        for man in self._table_men:
            while man is not None:
                woman: Sym = self._table_men[man][man_individual_score[man]]
                curr_husband: Sym|None = inv_matching[woman]    
                if self._rank_men[woman][man] < self._rank_men[woman][curr_husband]:
                    matching[man] = woman
                    man, inv_matching[woman] = inv_matching[woman], man
                if man is not None: man_individual_score[man] += 1
        return matching

class Stable_Marriage_Random_Tables(Stable_Marriage):
    def __init__(self,n: int) -> None:
        table_men: Table   = self.generate_random_table(n)
        table_women: Table = self.generate_random_table(n)
        super().__init__(table_men, table_women)

    def generate_random_table(self,n: int) -> Table:
        return {i:random.sample(range(n) ,n) for i in range(n)} 

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
    s.print_tables()
    # print(s.get_ranking(s._table_men))
    # print(s.get_ranking(s._table_women))
    opt_matching: Dict[Sym,Sym] = s.solve_problem()
    print(f"Matching found: {opt_matching}")
    print(f"Matching is stable? {s.matching_is_stable(opt_matching)}")
    print(f"Score for (men,women) is {s.compute_score(opt_matching)}")