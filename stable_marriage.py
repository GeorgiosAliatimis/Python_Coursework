import random
from collections.abc import Sequence
from tabulate import tabulate
from typing import Iterable, Dict, List, Sequence, Any, Tuple

Sym: Any = int | str
Table = Dict[Sym,Sequence[Sym]]
class Stable_Marriage:
    ''' 
    This class can solve the Stable Marriage Problem.
    It takes two preference tables as dictionaries with preference lists as values. 
    Men's/proposer's preference table lists the preferences in women/acceptors of each man/proposer
    i.e. table[man] is a list of preferences for man.
    Equivalently women's/acceptors' preference tables are given.
    
    Properties:
        _table_men: Table   (preference table of men)
        _table_women: Table (preference table of women)
        _rank_men: Dict[Sym,Dict[Sym|None,int]]  (rank of men for each woman, with undesirable man being denoted as None)
        _rank_women: Dict[Sym,Dict[Sym|None,int]]  (rank of women for each man, with undesirable woman being denoted as None)
    '''
    def __init__(self, table_men: Table, 
                       table_women: Table) -> None:
        '''table_men and table_woman are validated and ranking are computed'''        
        assert self.validate_table(table_men), 'Value of table_men is not valid'
        assert self.validate_table(table_women), 'Value of table_women is not valid'
        assert self.validate_table_no_duplicates(table_men), \
            'table_men has duplicate values in a preference list.'
        assert self.validate_table_no_duplicates(table_women), \
            'table_women has duplicate values in a preference list.'
        assert self.validate_tables_share_symbols(table_men,table_women), \
            'Values of table_men and table_women are valid but there is a symbol mismatch'
        self._table_men: Table   = table_men 
        self._table_women: Table = table_women
        self._rank_women: Dict[Sym,Dict[Sym|None,int]] = self.compute_ranking(self._table_men)
        self._rank_men: Dict[Sym,Dict[Sym|None,int]] = self.compute_ranking(self._table_women)

    def compute_ranking(self,table: Table) -> Dict[Sym,Dict[Sym|None,int]]: 
        '''
        Returns a version of the table where the list (values of the dictionary) are inverted.
        A preference list ["a","b","c"] becomes a ranking dictionary {"a":1,"b":2,"c":3} 
        so that output[X][y] is the ranking of y according to X.
        Rankings begin from zero.
        '''
        return {key: {v:i for i,v in enumerate(val)} | {None:len(val)}  for key,val in table.items()}

    def validate_table_no_duplicates(self,table: Table) -> bool:
        '''Validates that the table has no duplicates in any of its preference lists'''
        return all(len(pref_list) == len(set(pref_list))  for pref_list in table.values())

    def validate_tables_share_symbols(self,table_men: Table, table_women: Table) -> bool:
        '''
        Validates that the tables share the same symbols in that for every
        preference list of a table there is a 1-1 mapping to the keys of the other table
        '''
        vals2_in_keys1: bool  =  all( set(x) == set(table_men.keys()) for x in table_women.values() )
        vals1_in_keys2: bool  =  all( set(x) == set(table_women.keys()) for x in table_men.values() )
        return vals1_in_keys2 and vals2_in_keys1

    def validate_table(self,table: Table) -> bool:
        '''Validates that a table has the right type and consistent dimension across all values of the dictionary'''
        is_right_type: bool=isinstance(table,dict) and  \
                            all(isinstance(x, Sequence) for x in table.values()) and \
                            all(all(isinstance(y, Sym.__args__) for y in x) for x in table.values())  
        if not is_right_type:   return False
        n: int = len(table[next(iter(table))])
        has_consistent_dimension: bool = all(len(x) == n for x in table.values())
        if not has_consistent_dimension: return False
        return True

    def matching_is_stable(self, matching: Dict[Sym,Sym]) -> bool:
        '''
        For a given matching (which is a dictionary with key=man and value=matched_woman) the algorithm 
        checks whether the matching is stable returning True if it is.
        '''
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
        '''
        Computes the score for men and women which is defined as the sum of all the rankings 
        for men and women respectively. The higher the score for a gender,
        the less the aggregate satisfaction for that gender. A score of zero corresponds to complete 
        satisfaction for that gender implying that every person from that gender got their first preference.
        The highest score is (n-1)*n which corresponds to every person from that gender getting their last preference,
        where n is the number of people from each gender.
        '''
        score_men: int 
        score_women: int 
        score_men = sum(self._rank_women[man][matching[man]] for man in self._table_men)
        score_women = sum(self._table_women[matching[man]].index(man) for man in self._table_men)
        return score_men, score_women

    def print_tables(self) -> None:
        '''Tables are printed using the tabulate library for pretty visualization'''
        n: int = len(self._table_men)
        t: Table
        for t in (self._table_men,self._table_women):
            matrix: List[List[Sym]] = [[k] + list(v) for k, v in t.items()]
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            headers: List[str] = [""] + [ordinal(i) for i in range(1,n+1)]
            print(tabulate( matrix,tablefmt="fancy_grid",headers=headers))

    def solve_problem(self) -> Dict[Sym,Sym]:
        '''
        The Stable Marriage Problem is solved using the algorithm descripted in Chapter 2 page 9
        of 'Stable Marriage and Its Relation to Other Combinatorial Problems'.
        A matching (as a dictionary) is returned.
        '''
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
    '''
    Random preference tables of size n are generated for both men/proposers and women/acceptors.
    All other methods inherited from Stable_Marriage.
    '''
    def __init__(self,n: int) -> None:
        table_men: Table   = self.generate_random_table(n)
        table_women: Table = self.generate_random_table(n)
        super().__init__(table_men, table_women)

    def generate_random_table(self,n: int) -> Table:
        return {i:random.sample(range(n) ,n) for i in range(n)} 

if __name__ == "__main__":
    # This is the example given in Ch1 and Ch2 of 
    # Stable Marriage and Its Relation to Other Combinatorial Problems.
    # The same matching is found {'A': 'd', 'B': 'a', 'C': 'b', 'D': 'c'}.
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
    opt_matching: Dict[Sym,Sym] = s.solve_problem()
    print(f"Matching found: {opt_matching}")
    print(f"Matching is stable? {s.matching_is_stable(opt_matching)}")
    print(f"Score for (men,women) is {s.compute_score(opt_matching)}")

    # We now run Stable_Marriage_Random_Tables which generates 
    # random preference tables for n=5 people of each gender. 
    print("-"*40)
    random.seed(1)
    r: Stable_Marriage_Random_Tables = Stable_Marriage_Random_Tables(5)
    r.print_tables()
    opt_matching_r: Dict[Sym,Sym] = r.solve_problem()
    print(f"Matching found: {opt_matching_r}")
    print(f"Matching is stable? {r.matching_is_stable(opt_matching_r)}")
    print(f"Score for (men,women) is {r.compute_score(opt_matching_r)}")