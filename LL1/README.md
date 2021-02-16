# A top-down implementation of LL(1) parser

## Description
Similar to another implementation in [224. Basic Calculator](https://leetcode.com/problems/basic-calculator/discuss/1022514/python-lexer-ll1-parser-with-parsing-table), but this one requires `lval` technique, I referred the solution provided by [dzd2018](https://leetcode.com/problems/basic-calculator-ii/discuss/297560/Top-Down-LL(1)-recursive-parser-(16ms)-easy-to-understand). This code is much harder to read by using many else rather than the explicit comparison, if you are new to compiler like me, please try to solve 224 first.

## First/Follow Table
Grammar | First | Follow
-|-|-
E -> TE' | NUM | $
E'-> None / +TE' / -TE' | +, -, None | $
T -> FT' | NUM | +, -, $
T'-> None / *FT' / /FT' | *, /, None | +, -, $
F -> -F / NUM | -, NUM | +, -, *, /, $

## Parsing Table

∅|NUM|+|-|*|/|$
-|-|-|-|-|-|-
E|TE'|||||
E'||+TE'|-TE'|||None
T|FT'|||||
T'||None|None|*FT'|/FT'|None
F|NUM||-F|||
