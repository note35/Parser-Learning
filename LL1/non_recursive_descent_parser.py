from typing import *
# https://leetcode.com/problems/basic-calculator-ii/discuss/1022609/Python-Lexer-%2B-LL(1)-Parser-with-parsing-table

parsing_table = {
    'E': {'N': ['T', 'Ep']},
    'Ep': {'+': ['+', 'T', 'Ep'], '-': ['-', 'T', 'Ep'], '$': []},
    'T': {'N': ['F', 'Tp']},
    'Tp': {'+': [], '-': [], '*': ['*', 'F', 'Tp'], '/': ['/', 'F', 'Tp'], '$': []},
    'F': {'N': ['N']}
}


class Node:
    def __init__(self, key=None, val=None, parent=None):
        self.key = key
        self.val = val
        self.parent = parent
        self.children = []

        
def to_key(symb):
    ''' helper function to convert int to symbol N '''
    return 'N' if symb not in ['+', '-', '*', '/', '$'] else symb


class NonRecursiveDescentParserLL1:
    def __init__(self, E: List[str]) -> None:
        self.E = E
        self.idx = 0
        root = Node('E')
        self.tree_root = root
        self.stack = ['$', root]
    
    def parse(self) -> Node:
        while self.stack[-1] != '$':
            cur_node = self.stack.pop()
            cur_non_term = cur_node.key
            cur_token = self.E[self.idx]
            if (cur_non_term == 'N' and type(cur_token) == int) or cur_non_term == cur_token:
                # terminal: int or +-*/
                self.idx += 1
                cur_node.val = cur_token
            else:
                # non-terminal: E, Ep, T, Tp, F
                new_symbs = parsing_table[cur_non_term][to_key(cur_token)].copy()
                if len(new_symbs) == 0:
                    cur_node.children.append(Node('None', None))
                else:
                    while new_symbs:
                        new_symb = new_symbs.pop()
                        new_node = Node(new_symb, parent=cur_node)
                        cur_node.children.append(new_node)
                        self.stack.append(new_node)
        return self.tree_root


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
        
    def calculate(self, s: str) -> Node:
        return NonRecursiveDescentParserLL1(self.lexer(s)).parse()
