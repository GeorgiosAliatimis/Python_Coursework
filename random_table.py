import random
from collections.abc import Sequence
from typing import Iterable, Dict, Sequence, Any
from table import Table

Sym: Any = int | str 

class Random_Table(Table): 
    def __init__(self,n: int, **kwargs ) -> None:
        table: Dict[int,Sequence[int]] = self.generate_random_table(n,**kwargs)
        super().__init__(table)

    def generate_random_table(self,n: int,key_syms: Iterable[Sym]|None = None , 
                                          val_syms: Sequence[Sym]|None = None) -> Dict[Sym,Sequence[Sym]]:
        '''
        Generates random preference tables of size n as a dictionary.
        If symbols are missing they are set to 0:n-1.
        '''
        if key_syms is None: key_syms = list(range(n))
        if val_syms is None: val_syms = list(range(n))
        return {i:random.sample(val_syms,n) for i in key_syms} 