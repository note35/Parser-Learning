# https://leetcode.com/problems/basic-calculator-ii/discuss/1054545/Python-Packrat-Parser-(Backtracking-%2B-Memo)

def t(f, *args):
    ''' helper function to ignore invalid cases '''
    try:
        return f(*args)
    except Exception as e:
        # print(e)  # debug
        return None
    

class PackratParser:
    def __init__(self, E: str) -> None:
        self.E = E
        self.dp = {
            'dvAdditive': {},
            'dvMultitive': {},
            'dvDecimal': {},
            'dvChar': {}
        }

    def parse(self):
        self._parse(0)
        return self.dp['dvAdditive'][0][0]
        
    def _parse(self, idx: int) -> None:
        # backtracking all cases
        if self.E[idx] != '$':
            t(self.pAdditive, idx)
            t(self.pMultitive, idx)
            t(self.pDecimal, idx)
            self._parse(idx+1)

    def pAdditive(self, idx) -> Tuple[int, int]:
        if idx in self.dp['dvAdditive']: return self.dp['dvAdditive'][idx]
        
        vleft, nidx = self.pMultitive(idx)
        if self.E[nidx] == '$':
            # Additive -> None
            ret = vleft, nidx
        else:
            # Additive -> +MultitiveAdditive | -MultitiveAdditive
            symb, nnidx = self.pChar(nidx)
            if symb == '+':
                vright, nnnidx = self.pAdditive(nnidx)
                ret = (vright + vleft, nnnidx)
            elif symb == '-':
                vright, nnnidx = self.pAdditive(nnidx)
                ret = (vright - vleft, nnnidx)
            else:
                ret = vleft, nidx

        self.dp['dvAdditive'][idx] = ret
        return ret
    
    def pMultitive(self, idx: int) -> Tuple[int, int]:
        if idx in self.dp['dvMultitive']: return self.dp['dvMultitive'][idx]

        vleft, nidx = self.pDecimal(idx)
        if self.E[nidx] == '$':
            # Multitive -> None
            ret = vleft, nidx
        else:
            # Multitive -> *DecimalMultitive | /DecimalMultitive
            symb, nnidx = self.pChar(nidx)
            if symb == '*':
                vright, nnnidx = self.pMultitive(nnidx)
                ret = (vright * vleft, nnnidx)
            elif symb == '/':
                vright, nnnidx = self.pMultitive(nnidx)
                ret = (vright // vleft, nnnidx)
            else:
                ret = vleft, nidx

        self.dp['dvMultitive'][idx] = ret
        return ret
    
    def pDecimal(self, idx: int) -> Tuple[int, int]:
        if idx in self.dp['dvDecimal']: return self.dp['dvDecimal'][idx]

        symb, nidx = self.pChar(idx)
        if type(symb) == int:
            # Decimal -> [0-9]+
            ret = symb, nidx
        else:
            raise ValueError('unable to parse decimal')

        self.dp['dvDecimal'][idx] = ret
        return ret
        
    def pChar(self, idx: int) -> Tuple[Union[int, str], int]:
        if idx in self.dp['dvChar']: return self.dp['dvChar'][idx]

        ret = self.lexer(idx)

        self.dp['dvChar'][idx] = ret
        return ret
    
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
            return int(num_pat[::-1]), idx
        else:
            raise ValueError('unable to parse input string by lexer')

class Solution:        
    def calculate(self, s: str) -> int:
        # trim space + right-to-left parsing
        return PackratParser(s.replace(' ', '')[::-1]+'$').parse()
