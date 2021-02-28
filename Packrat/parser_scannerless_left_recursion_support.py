from collections import defaultdict
from typing import *


def t(f, *args):
    ''' helper function to ignore invalid cases '''
    try:
        f(*args)
    except Exception as e:
        # print(e)  # debug
        pass


def memo(func):
    def memo_wrapper(self, pos):
        if pos in self.dp[func.__name__]:
            return self.dp[func.__name__][pos]
        self.dp[func.__name__][pos] = func(self, pos)
        return self.dp[func.__name__][pos]
    return memo_wrapper


def memo_left_rec(func):
    # https://medium.com/@gvanrossum_83706/left-recursive-peg-grammars-65dab3c580e1
    def memo_left_rec_wrapper(self, pos):
        if pos in self.dp[func.__name__]:
            return self.dp[func.__name__][pos]

        self.dp[func.__name__][pos] = lastres, lastpos = None, pos
        while True:
            res, endpos = func(self, pos)
            if endpos <= lastpos:
                break
            self.dp[func.__name__][pos] = lastres, lastpos = res, endpos
        return lastres, lastpos
    return memo_left_rec_wrapper


class PackratParser:
    def __init__(self, E: str) -> None:
        self.E = E
        self.dp = defaultdict(dict)

    def parse(self):
        return self.pAdditive(0)[0]

    @memo_left_rec
    def pAdditive(self, idx) -> Tuple[int, int]:
        try:
            vleft, nidx = self.pAdditive(idx)
            symb, nnidx = self.pChar(nidx)
            vright, nnnidx = self.pMultitive(nnidx)
            if symb == '+':  # Additive -> Additive + Multitive
                return vleft + vright, nnnidx
            if symb == '-':  # Additive -> Additive - Multitive
                return vleft - vright, nnnidx
            raise Exception('failed to run above derivation')
        except:
            return self.pMultitive(idx)  # Additive -> Multitive

    @memo_left_rec
    def pMultitive(self, idx: int) -> Tuple[int, int]:
        try:
            vleft, nidx = self.pMultitive(idx)
            symb, nnidx = self.pChar(nidx)
            vright, nnnidx = self.pDecimal(nnidx)
            if symb == '*':  # Multitive -> Multitive * Decimal
                return vleft * vright, nnnidx
            if symb == '/':  # Multitive -> Multitive / Decimal
                return vleft // vright, nnnidx
            raise Exception('failed to run above derivation')
        except:
            return self.pDecimal(idx)  # Multitive -> Decimal

    @memo
    def pDecimal(self, idx: int) -> Tuple[int, int]:
        return self.pChar(idx)
    
    @memo
    def pChar(self, idx: int) -> Tuple[Union[int, str], int]:
        return self.lexer(idx)
    
    @memo
    def lexer(self, idx: int) -> Tuple[Union[int, str], int]:
        # scannerless implementation
        if self.E[idx] in '+-*/':
            return self.E[idx], idx+1
        elif self.E[idx] in '1234567890':
            num_pat = self.E[idx]
            idx += 1
            while idx < len(self.E) and self.E[idx] in '1234567890':
                num_pat += self.E[idx]
                idx += 1
            return int(num_pat), idx
        else:
            raise ValueError('unable to parse input string by lexer')


class Solution:        
    def calculate(self, s: str) -> int:
        # trim space + left-to-right parsing
        return PackratParser(s.replace(' ', '')+'$').parse()
