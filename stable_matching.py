import random
from typing import Iterable, Dict, Any, Tuple
from table import Table
from random_table import Random_Table

Sym: Any = int | str | None

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
        score_acceptor: int = sum(self.acceptor.rank[matching[prop]][prop] for prop in self.proposer)
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