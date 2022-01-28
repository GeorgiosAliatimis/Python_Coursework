import random
from collections.abc import Sequence
from tabulate import tabulate
from typing import Iterable, Dict, List, Sequence, Any, Tuple

Sym: Any = int | str

class Table(dict):
    '''
    This class represents the preference tables that are used in the 
    Stable Matching Problem. 
    '''
    def __init__(self, table: Any):
        super().__init__(table)
        self.validator()
        
    def validator(self) -> None:
        assert self.right_type(), 'Input does not have right type'
        assert self.consistent_dimension(), 'Input table has preference lists of different length'
        assert self.no_duplicates(), 'Input has duplicate values in a preference list.'
    
    def right_type(self) -> bool:
        '''Assesses whether table is of the right type'''
        return isinstance(self,dict) and  \
                all(isinstance(x, Sequence) for x in self.values()) and \
                all(all(isinstance(y, Sym.__args__) for y in x) for x in self.values())
    
    def consistent_dimension(self) -> bool: 
        '''Assesses whether the table preference lists have consistent dimensions'''
        n: int = len(self)
        return all(len(x) == n for x in self.values())
        
    def no_duplicates(self) -> bool:
        '''Checks whether preference lists contain any duplicates'''
        return all(len(pref_list) == len(set(pref_list))  for pref_list in self.values())
    
    def get_rank(self) -> None: 
        '''
        Creates a version of the table where the preference lists (values of the dictionary) are inverted.
        A preference list ["a","b","c"] becomes a ranking dictionary {"a":1,"b":2,"c":3} 
        so that output[X][y] is the ranking of y according to X.
        Rankings begin from zero.
        '''
        self.rank = {key: {v:i for i,v in enumerate(val)} | {None:len(val)}  for key,val in self.items()}
    
    def __repr__(self) -> str:
        '''
        Tables are printed using the tabulate library for pretty visualization
        '''
        n: int = len(self)
        matrix: List[List[Sym]] = [[k] + list(v) for k, v in self.items()]
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        headers: List[str] = [""] + [ordinal(i) for i in range(1,n+1)]
        return str(tabulate(matrix,tablefmt="fancy_grid",headers=headers))


class Random_Table(Table): 
    def __init__(self,n: int) -> None:
        table: Dict[int,Sequence[int]] = self.generate_random_table(n)
        super().__init__(table)

    def generate_random_table(self,n: int) -> Dict[Sym,Sequence[Sym]]:
        return {i:random.sample(range(n) ,n) for i in range(n)} 

class Stable_Matching:
    ''' 
    This class solves the Stable Matching Problem.
    It takes two preference tables (proposer,acceptor) with preference lists as values. 
    '''
    def __init__(self, proposer: Table, 
                       acceptor: Table) -> None:  
        assert isinstance(proposer,Table), 'Proposer is not a Table'   
        assert isinstance(acceptor,Table), 'Acceptor is not a Table' 
        for t in (proposer,acceptor):   t.get_rank()
        self.proposer: Table = proposer 
        self.acceptor: Table = acceptor
        assert self.validate_tables_share_symbols(), 'Symbol mismatch between proposer and acceptor'

    def validate_tables_share_symbols(self) -> bool:
        '''
        Validates that the tables share the same symbols in that for every
        preference list of a table there is a 1-1 mapping to the keys of the other table
        '''
        vals2_in_keys1: bool  =  all( set(x) == set(self.proposer.keys()) for x in self.acceptor.values() )
        vals1_in_keys2: bool  =  all( set(x) == set(self.acceptor.keys()) for x in self.proposer.values() )
        return vals1_in_keys2 and vals2_in_keys1

    def matching_is_stable(self, matching: Dict[Sym,Sym]) -> bool:
        '''
        For a given matching (which is a dictionary with key=proposer and value=matched_acceptor)
        the algorithm checks whether the matching is stable returning True if it is.
        '''
        acc: Sym   #Acceptor
        prop: Sym  #Proposer
        props: Iterable[Sym] 
        for acc, props in self.acceptor.items():
            for prop in props:
                if acc == matching[prop]:  break
                curr_acc: Sym = matching[prop]
                if self.proposer.rank[prop][acc] < self.proposer.rank[prop][curr_acc]:   
                    return False
        return True

    def compute_score(self, matching: Dict[Sym,Sym]) -> Tuple[int,int]:
        '''
        Computes the score for proposers and acceptors which is defined as the sum of all the rankings 
        for proposers and acceptors respectively. The higher the score for a group,
        the less the aggregate satisfaction for that group. A score of zero corresponds to complete 
        satisfaction for that group implying that every member of that group got their first preference.
        The highest score is (n-1)*n which corresponds to every member of that group getting their last preference,
        where n is the number of proposers and acceptors.
        '''
        score_proposer: int = sum(self.proposer.rank[prop][matching[prop]] for prop in self.proposer)
        score_acceptor: int = sum(self.acceptor[matching[prop]].index(prop) for prop in self.proposer)
        return score_proposer, score_acceptor

    def solve_problem(self) -> Dict[Sym,Sym]:
        '''
        The Stable Matching Problem is solved using the algorithm descripted in Chapter 2 page 9
        of 'Stable Marriage and Its Relation to Other Combinatorial Problems'.
        A matching (as a dictionary) is returned.
        '''
        prop_individual_score: Dict[Sym,int] = {prop:0 for prop in self.proposer}
        matching: Dict[Sym,Sym|None] = {prop: None for prop in self.proposer}
        inv_matching: Dict[Sym,Sym|None] = {acc: None for acc in self.acceptor}
        prop: Sym|None
        for prop in self.proposer:
            while prop is not None:
                acc: Sym = self.proposer[prop][prop_individual_score[prop]]
                curr_prop: Sym|None = inv_matching[acc]    
                if self.acceptor.rank[acc][prop] < self.acceptor.rank[acc][curr_prop]:
                    matching[prop] = acc
                    prop, inv_matching[acc] = inv_matching[acc], prop
                if prop is not None: prop_individual_score[prop] += 1
        return matching

if __name__ == "__main__":
    # Two examples are shown; a predefined example given in Ch1 and Ch2 of 
    # Stable Marriage and Its Relation to Other Combinatorial Problems.
    # The same matching is found {'A': 'd', 'B': 'a', 'C': 'b', 'D': 'c'}.
    p1: Table = Table({'A': ['c', 'b', 'd', 'a'], 'B': ['b', 'a', 'c', 'd'], \
        'C': ['b', 'd', 'a', 'c'], 'D': ['c', 'a', 'd', 'b']})
    a1: Table =  Table({'a': ['A', 'B', 'D', 'C'], 'b': ['C', 'A', 'D', 'B'], \
        'c': ['C', 'B', 'D', 'A'], 'd': ['B', 'A', 'C', 'D']})
    #The second example is random with n=5 proposers and acceptors.
    random.seed(1)
    p2: Table = Random_Table(n=5)
    a2: Table = Random_Table(n=5)

    for proposer, acceptor in [(p1,a1),(p2,a2)]:
        print("Proposer table")
        print(proposer)
        print("Acceptor Table")
        print(acceptor)
        s: Stable_Matching = Stable_Matching(proposer,acceptor)
        opt_matching: Dict[Sym,Sym] = s.solve_problem()
        print(f"Matching found: {opt_matching}")
        print(f"Matching is stable? {s.matching_is_stable(opt_matching)}")
        print(f"Score for (proposers,acceptors) is {s.compute_score(opt_matching)}")