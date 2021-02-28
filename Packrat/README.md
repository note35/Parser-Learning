# Implementation based on Bryan Ford's packrat parser (scannerless)

## Description

This folder contains 3 implementation:
- **parser_scannerless.py**: an implementation based on Bryan Ford's first paper.
- **parser_scannerless_with_memo.py**: a modified implementation based on **parser_scannerless.py**.
- **parser_scannerless_left_recursion_support.py**: an additional implementation with left-recursion support.

---

- **parser_scannerless.py** and **parser_scannerless_with_memo.py** are the naive and cheated version without left-recursion support. The implementation is based on the first paper [Packrat Parsing: Simple, Powerful, Lazy, Linear Time](https://pdos.lcs.mit.edu/~baford/packrat/icfp02/) by Bryan Ford. You can check the page to see the paper and the [Haskell version of implementation](https://pdos.lcs.mit.edu/~baford/packrat/icfp02/ArithPackrat.hs).
  - In the first version of implementation, both lexer (1104ms) and lexerless (872ms) versions of the code's performance are relatively slow compared with [LL(1) version](https://leetcode.com/problems/basic-calculator-ii/discuss/1022609/python-lexer-ll1-parser-with-parsing-table) (216ms).
  - The cheated trick I made is to scan the input string from right to left to handle symbols `-` and `/`. So, **left-recursion** here is actually **right-recursion**, and the grammar has no **right-recursion**.
  - The cheated trick is hard to apply to another question, [Basic Calculator](https://leetcode.com/problems/basic-calculator/), because it needs to further handle the special cases like `-2 + 1` and `-(-2)`, for right-to-left parsing, `2-` and `(-` requires special lookahead to handle. (Or, a special lexer may work as well.) 

- **parser_scannerless_left_recursion_support.py** is based on [Guido's blog](https://medium.com/@gvanrossum_83706/left-recursive-peg-grammars-65dab3c580e1) along with two papers [1](https://arxiv.org/pdf/1207.0443.pdf) and [2](http://web.cs.ucla.edu/~todd/research/pepm08.pdf). As the name suggests, it supports left-recursion.

## Grammar

```
Additive -> Additive + Multitive | Additive - Multitive | Multitive
Multitive -> Multitive + Decimal | Multitive - Decimal | Decimal
Decimal -> [0-9]+
```
