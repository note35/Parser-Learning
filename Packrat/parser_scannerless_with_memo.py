from collections import defaultdict
from typing import *


def t(f, *args):
    ''' helper function to ignore invalid cases '''
    try:
        return f(*args)
    except Exception as e:
        # print(e)  # debug
        return None


def memo(func):
    def memo_wrapper(self, pos):
        if pos in self.dp[func.__name__]:
            return self.dp[func.__name__][pos]
        self.dp[func.__name__][pos] = func(self, pos)
        return self.dp[func.__name__][pos]
    return memo_wrapper
    

class PackratParser:
    def __init__(self, E: str) -> None:
        self.E = E
        self.goal = 'pAdditive'  # same as 'dvAdditive' in paper
        self.dp = defaultdict(dict)

    def parse(self):
        self._parse(0)
        return self.dp[self.goal][0][0]
        
    def _parse(self, idx: int) -> None:
        # backtracking all cases
        if self.E[idx] != '$':
            t(self.pAdditive, idx)
            t(self.pMultitive, idx)
            t(self.pDecimal, idx)
            self._parse(idx+1)

    @memo
    def pAdditive(self, idx) -> Tuple[int, int]:
        vleft, nidx = self.pMultitive(idx)
        if self.E[nidx] == '$':  # Additive -> Multitive
            return vleft, nidx

        symb, nnidx = self.pChar(nidx)
        if symb not in '+-':
            return vleft, nidx

        vright, nnnidx = self.pAdditive(nnidx)
        if symb == '+':  # Additive -> Additive + Multitive
            return vright + vleft, nnnidx
        if symb == '-':  # Additive -> Additive - Multitive
            return vright - vleft, nnnidx

    @memo
    def pMultitive(self, idx: int) -> Tuple[int, int]:
        vleft, nidx = self.pDecimal(idx)
        if self.E[nidx] == '$':  # Multitive -> Decimal
            return vleft, nidx

        symb, nnidx = self.pChar(nidx)
        if symb not in '*/':
            return vleft, nidx

        vright, nnnidx = self.pMultitive(nnidx)
        if symb == '*':  # Multitive -> Multitive * Decimal
            return vright * vleft, nnnidx
        if symb == '/':  # Multitive -> Multitive / Decimal
            return vright // vleft, nnnidx
    
    @memo
    def pDecimal(self, idx: int) -> Tuple[int, int]:
        return self.pChar(idx)
    
    @memo
    def pChar(self, idx: int) -> Tuple[Union[int, str], int]:
        return self.lexer(idx)
    
    def lexer(self, idx: int) -> Tuple[Union[int, str], int]:
        # scannerless implementation
        if self.E[idx] in '+-*/':
            return self.E[idx], idx+1
        elif self.E[idx] in '1234567890':
            num_pat = self.E[idx]
            idx += 1
            while idx < len(self.E) and self.E[idx] in '1234567890':
                num_pat = self.E[idx] + num_pat
                idx += 1
            return int(num_pat), idx
        else:
            raise ValueError('unable to parse input string by lexer')


class Solution:        
    def calculate(self, s: str) -> int:
        # trim space + right-to-left parsing
        return PackratParser(s.replace(' ', '')[::-1]+'$').parse()
