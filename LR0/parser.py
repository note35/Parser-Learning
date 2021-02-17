# https://leetcode.com/problems/basic-calculator-ii/discuss/1068095/Python-Lexer-%2B-LR(0)-Parser-with-DFA-and-parsing-table

# (number of popped symb, derived symb)
reduce_rules = {
    1: (0, 'Done'),  # E'-> E
    2: (3, 'E'),     # E -> E+T
    3: (3, 'E'),     # E -> E-T
    4: (1, 'E'),     # E -> T
    5: (3, 'T'),     # T -> T*N
    6: (3, 'T'),     # T -> T/N
    7: (1, 'T')      # T -> N
}

# negative => reduce / positive => shift
parsing_table = {
    1: {'N': 12, 'E': 2, 'T': 3},
    2: {'+': 4, '-': 5, '$': -1},
    3: {'+': -4, '-': -4, '$': -4, '*': 8, '/': 9, 'N': -4},
    4: {'N': 12, 'T': 6},
    5: {'N': 12, 'T': 7},
    6: {'+': -2, '-': -2, '$': -2, '*': 8, '/': 9, 'N': -2},
    7: {'+': -3, '-': -3, '$': -3, '*': 8, '/': 9, 'N': -3},
    8: {'N': 10},
    9: {'N': 11},
    10:{'+': -5, '-': -5, '$': -5, '*': -5, '/': -5, 'N': -5},
    11:{'+': -6, '-': -6, '$': -6, '*': -6, '/': -6, 'N': -6},
    12:{'+': -7, '-': -7, '$': -7, '*': -7, '/': -7, 'N': -7},
}

class ParserLR0:
    def __init__(self, E: str) -> None:
        self.E = E
        self.pos = 0
        self.states = [1]  # set initial state to 1
        self.symbs = []  # Example value => [('N', 1), ('+', '+')]
        
    def symb2key(self, symb: str) -> str:
        # raw symb can only be either '+-*/' or 'N'
        return symb if symb in ['$', '+', '-', '*', '/'] else 'N'

    def parse(self):
        while True:
            symb = self.E[self.pos]
            nxt_state = parsing_table[self.states[-1]][self.symb2key(symb)]
            if nxt_state > 0:
                # shift
                self.states.append(nxt_state)
                self.symbs.append(symb)
                self.pos += 1
            else:
                # reduce
                pop_n, derived_symb = reduce_rules[-nxt_state]
                if pop_n == 0:
                    # assume all input is valid, symbs will leave the answer
                    return self.symbs[0]
                else:
                    if pop_n == 1:  # simple reduction
                        # reduce states
                        self.states.pop()
                        self.states.append(parsing_table[self.states[-1]][derived_symb])
                        # derivation
                        # Since reduce from T -> N and E -> T don't change the symbol value
                        # namely, self.symbs.append(self.symbs.pop()) == pass
                    elif pop_n == 3:  # operator reduction
                        # reduce states
                        self.states = self.states[:-2]  # pop 2 states
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
        return ParserLR0(self.lexer(s)).parse()
