from typing import *
# https://leetcode.com/problems/basic-calculator-ii/discuss/1069679/Python-Lexer-%2B-Operator-Precedence-Parser-with-steps

# key: symb / val: number of popped symb
reduce_rules = {
    'N': 1,
    '+': 3,
    '-': 3,
    '*': 3,
    '/': 3
}

# when precedence is same, the precedence of IN will always higher than OUT and take reduce action
precedence_table = {
    'IN': {'N': 8, '+': 2, '-': 2, '*': 4, '/': 4, '$': 0},
    'OUT':{'N': 8, '+': 1, '-': 1, '*': 3, '/': 3, '$': 0}
}

class OperatorPrecedenceParser:
    def __init__(self, E: str) -> None:
        self.E = E
        self.pos = 0
        self.stack = ['$']  # set initial symbol to '$'
        self.symbs = []
        
    def symb2key(self, symb: str) -> str:
        # raw symb can only be either '+-*/' or 'N'
        return symb if symb in ['$', '+', '-', '*', '/'] else 'N'

    def parse(self):
        while True:
            in_symb = self.stack[-1]
            out_symb = self.symb2key(self.E[self.pos])
            if in_symb == out_symb == '$':
                return self.symbs[0]
            if precedence_table['IN'][in_symb] < precedence_table['OUT'][out_symb]:
                # shift
                self.stack.append(out_symb)
                self.symbs.append(self.E[self.pos])
                self.pos += 1
            else:
                # reduce
                pop_n = reduce_rules[self.stack.pop()]
                if pop_n == 1:  # simple reduction
                    pass                    
                elif pop_n == 3:  # operator reduction
                    # derivation: get lval, operator, and rval => calculate the result
                    lval, operator, rval = self.symbs[-3:]
                    self.symbs = self.symbs[:-3]  # pop 3 symbols
                    if operator == '+':
                        self.symbs.append(lval + rval)
                    elif operator == '-':
                        self.symbs.append(lval - rval)
                    elif operator == '*':
                        self.symbs.append(lval * rval)
                    elif operator == '/':
                        self.symbs.append(lval // rval)


class Solution:    
    def lexer(self, s: str) -> List[str]:
        symbs, idx = [], 0
        while idx < len(s):
            if s[idx] in '+-*/':
                symbs.append(s[idx])
                idx += 1
            elif s[idx] in '1234567890':
                num_pat = s[idx]
                idx += 1
                while idx < len(s) and s[idx] in '1234567890':
                    num_pat += s[idx]
                    idx += 1
                symbs.append(int(num_pat))
            else:
                idx += 1
        symbs.append('$')
        return symbs
    
    def calculate(self, s: str) -> int:
        return OperatorPrecedenceParser(self.lexer(s)).parse()
