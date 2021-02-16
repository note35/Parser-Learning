# https://leetcode.com/problems/basic-calculator-ii/discuss/1068095/Python-Lexer-%2B-LR(0)-Parser-with-DFA-and-parsing-table

# For non-operator => (number of symb , reduced state, None)
# For operator => (number of number, operator, reduced state)
reduce_rules = {
    1: (0, 'Done', None),
    2: (3, '+', 'E'),
    3: (3, '-', 'E'),
    4: (1, 'E', None),
    5: (3, '*', 'T'),
    6: (3, '/', 'T'),
    7: (1, 'T', None)
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
        self.states = [1]
        self.symbs = []  # Example value => [('N', 1), ('+', '+')]
        
    def symb2key(self, symb: str) -> str:
        # raw symb can only be either '+-*/' or 'N'
        return symb if symb in ['$', '+', '-', '*', '/'] else 'N'

    def parse(self) -> int:
        while True:
            symb = self.E[self.pos]
            nxt_state = parsing_table[self.states[-1]][self.symb2key(symb)]
            if nxt_state > 0:
                # shift
                self.states.append(nxt_state)
                self.symbs.append((self.symb2key(symb), symb))
                self.pos += 1
            else:
                # reduce
                pop_n, action, nxt_key = reduce_rules[-nxt_state]
                if action == 'Done':
                    # assume all input is valid, symbs will leave the answer
                    return self.symbs[0][1]
                else:
                    if pop_n == 1:  # simple reduction based on parsing table
                        # reduce states
                        prev_state = self.states.pop()
                        self.states.append(parsing_table[self.states[-1]][action])
                        # derivation 
                        _, prev_symb = self.symbs.pop()
                        self.symbs.append((action, prev_symb))
                    elif pop_n == 3:  # operator reduction based on parsing table
                        # reduce states
                        prev_state = self.states.pop()
                        prev_state = self.states.pop()
                        # get lval and rval + calculate the result + derivation
                        rkey, rval = self.symbs.pop()
                        _, _ = self.symbs.pop()  # don't care operator, we actually don't need store it as symbol
                        lkey, lval = self.symbs.pop()
                        if action == '+':
                            self.symbs.append((nxt_key, lval + rval))
                        elif action == '-':
                            self.symbs.append((nxt_key, lval - rval))
                        elif action == '*':
                            self.symbs.append((nxt_key, lval * rval))
                        elif action == '/':
                            self.symbs.append((nxt_key, lval // rval))


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
