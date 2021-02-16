# Implementation based on Bryan Ford's packrat parser (scannerless)

## Description

This implementation is based on the paper [Packrat Parsing: Simple, Powerful, Lazy, Linear Time](https://pdos.lcs.mit.edu/~baford/packrat/icfp02/) by Bryan Ford. You can check the page to see the paper and the [Haskell version of implementation](https://pdos.lcs.mit.edu/~baford/packrat/icfp02/ArithPackrat.hs).

Note
- Both lexer (1104ms) and lexerless (872ms) version of the code's performance are relatively slow comparing with [LL(1) version](https://leetcode.com/problems/basic-calculator-ii/discuss/1022609/python-lexer-ll1-parser-with-parsing-table) (216ms). Below is the one without a lexer.
- The paper's example only supports `+` and `*` which are unaware of right-to-left / left-to-right. When adding symbol `-` and `/`, it forces the situation to be right-to-left, which makes the implementation a bit more tricky.  
- Because of right-to-left design, the implementation needs tons of modification to support another question [Basic Calculator](https://leetcode.com/problems/basic-calculator/) to handle the special cases like `-2 + 1` and `-(-2)`, for right-to-left parsing, `2-` and `(-` requires special lookahead to handle. (Or, a special lexer may work as well.) 

## Grammar

*Original*
```
Additive -> Additive + Multitive | Additive - Multitive | Multitive
Multitive -> Multitive + Decimal | Multitive - Decimal | Decimal
Decimal -> [0-9]+
```

*No left recursion*
```
Expression -> DecimalAdditive
Additive -> +MultitiveAdditive | -MultitiveAdditive | None
Multitive -> *DecimalMultitive | /DecimalMultitive | None
Decimal -> [0-9]+
```
