# https://leetcode.com/problems/basic-calculator-ii/discuss/1022609/Python-Lexer-%2B-LL(1)-Parser-with-parsing-table

class ParserLL1:
    def __init__(self, E: List[str]) -> None:
        self.E = E
        self.idx = 0
    
    def parse(self) -> int:
        return self.parse_E()
    
    def parse_E(self) -> int:
        return self.parse_Ep(self.parse_T())
    
    def parse_Ep(self, lval: int) -> int:
        cur_symb = self.E[self.idx]
        if cur_symb in '+-':
            self.idx += 1
            if cur_symb == '+':
                return self.parse_Ep(lval + self.parse_T())
            if cur_symb == '-':
                return self.parse_Ep(lval - self.parse_T())
        else:
            return lval

    def parse_T(self) -> int:
        return self.parse_Tp(self.parse_F())
        
    def parse_Tp(self, lval: int) -> int:
        cur_symb = self.E[self.idx]
        if cur_symb in '*/':
            self.idx += 1
            if cur_symb == '*':
                return self.parse_Tp(lval * self.parse_F())
            if cur_symb == '/':
                return self.parse_Tp(lval // self.parse_F())
        else:
            return lval

    def parse_F(self) -> int:
        cur_symb = self.E[self.idx]
        self.idx += 1
        if type(cur_symb) == int:
            return cur_symb
        if cur_symb == '-':
            return -self.parse_F()
        raise ValueError('Invalid Expression')


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
        return ParserLL1(self.lexer(s)).parse()
