from collections.abc import Sequence
from tabulate import tabulate
from typing import List, Sequence, Any

Sym: Any = int | str

def freeze(fun):
    '''
    Decorator that freezes a function and throws an error
    whenever this function is called.
    '''
    def ans(*args,**kwargs):
        raise Exception(f"Method {fun.__name__} is frozen.")
    return ans

class Table(dict):
    '''
    This class represents the preference tables that are used in the 
    Stable Matching Problem. 
    '''
    def __init__(self, table: Any):
        super().__init__(table)
        self.validator()
        #We now freeze all setter methods of dict so that the table does not change
        self.update = freeze(self.update)
        self.setdefault = freeze(self.setdefault)
        #set.__setitem__ = freeze(self.__setitem__)
    
    #For some strange reason, passing __setitem__ to the freeze decorator does not make it frozen;
    #In particular if we run obj.__setitem__(key,val) it does through "Method __setitem__ is frozen." 
    #but setting obj[key]=val is still allowed! By making its own function definition, it is frozen in both cases
    #and doesn't seem to interfere with the dictionary initialization.
    def __setitem__(self,*args,**kwargs):
        raise Exception("Method __setitem__ is frozen.")

    def validator(self) -> None:
        assert self.right_type(), 'Input does not have right type.'
        assert self.consistent_dimension(), 'Input table has a preference list that is not equal to the number of keys.'
        assert self.no_duplicates(), 'Input has duplicate values in a preference list.'
        assert self.same_symbols(), 'Preference lists do not share the same symbols.'
    
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
    
    def same_symbols(self) -> bool:
        '''Checks whether preference lists share the same symbols.'''
        prev = None
        for v in self.values():
            if prev is not None and set(v) != prev: return False
            prev = set(v)
        return True
    
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