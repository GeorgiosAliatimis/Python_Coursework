from math import comb
from itertools import combinations
from typing import Set

def assertions(num:int) -> None:
    '''
    Input: num 
    This function asserts whether the input num is a positive integer
    '''
    assert isinstance(num,int), "Input to binary_digit_sum should be int"
    assert num > 0, "Input integer should be positive"

def binary_digit_sum(num: int) -> int:
    ''' 
    Input: num 
    Output: sum of digits of num in binary. 
    Example: num = 12 (base 10) = 1100 (base 2) => output 1+1+0+0 = 2
    '''
    assertions(num)
    res = 0
    while num:  num, res = num//2, res + num%2
    return res

def binary_array(num: int) -> list[str]:
    '''
    Input: num 
    Output: list of digits of num in binary.
    Example: num = 12 (base 10) = 1100 (base 2) => output ['1', '1', '0', '0']
    '''
    assertions(num)
    return list(bin(num)[2:])

def num_comb_group_in_half(k: int) -> int:
    '''
    There are 2k people in a group, k>0. 
    Output: Number of ways of spliting the group to two equally sized groups of k people.
    '''
    assertions(k)
    # There are n choose m ways to split a group of n people into groups of m and n-m. 
    # Hence our answer is 2k choose k.
    return comb(2*k,k)

def pairs_group_in_half(k: int) -> list[list[Set[int]]]:
    '''
    There are 2k people in a group, k>0. 
    Output: List of all possible pairs 
    Example: for k=1=> 2 people the list of possible pairs is 
    [ [ {0}, {1}], [{1} , {0}] ]
    '''
    assertions(k)
    assert k <= 10, "Splitting a group of more than 20 people results in more than 7*10^5 pairs! Decrease k."
    group = set(range(2*k))
    return [[ set(c) , group - set(c) ] for c in  combinations(range(2*k),k)]

if __name__ == "__main__":
    # Binary representations
    num = 12
    print("The binary digit sum of {} is {}.".format(num,binary_digit_sum(num)))
    print("The binary array representation of {} is {}.".format(num,binary_array(num)))
    # Groups of people
    k = 2
    print("There are {} ways of splitting a group of {} people in groups of {}.".format(
        num_comb_group_in_half(k), 2* k, k
    ))
    print("Those pairs are {}".format(pairs_group_in_half(k)))