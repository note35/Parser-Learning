# A top-down implementation of LL(1) parser

## Description
There're 2 popular ways to implement LL(1) parser, recursive descent parser (top down) and [non-recursive descent](https://www.geeksforgeeks.org/algorithm-for-non-recursive-predictive-parsing/) (with parsing table and stack).

The recursive descent parser is straightforward and similar to my another implementation in [224. Basic Calculator](https://leetcode.com/problems/basic-calculator/discuss/1022514/python-lexer-ll1-parser-with-parsing-table). Note that this one requires `lval` technique, I referred the solution provided by [dzd2018](https://leetcode.com/problems/basic-calculator-ii/discuss/297560/Top-Down-LL(1)-recursive-parser-(16ms)-easy-to-understand).

The non-recursive descent parser instead, requires to build a parsing table based on **First** and **Follow**, and the return of non-recursive descent parser is a Concrete Syntax Tree instead of directly generating the result. You can refer to [this material](https://www.cs.purdue.edu/homes/xyzhang/spring11/notes/ll.pdf) for details.

## First/Follow Table
Grammar | First | Follow
-|-|-
E -> TE' | NUM | $
E'-> None / +TE' / -TE' | +, -, None | $
T -> FT' | NUM | +, -, $
T'-> None / *FT' / /FT' | *, /, None | +, -, $
F -> NUM | NUM | +, -, *, /, $

## Parsing Table

∅|NUM|+|-|*|/|$
-|-|-|-|-|-|-
E|TE'|||||
E'||+TE'|-TE'|||None
T|FT'|||||
T'||None|None|*FT'|/FT'|None
F|NUM|||||

## Examples

### `2 + 3 * 4`

```
STACK             | INPUT       | ACTION
------------------------------------------------------------
[$, E]            | 2 + 3 * 4 $ | Reduce: E -> TE'
[$, E', T]        | 2 + 3 * 4 $ | Reduce: T -> FT'
[$, E', T', F]    | 2 + 3 * 4 $ | Reduce: F -> N
[$, E', T', N]    | 2 + 3 * 4 $ | Shift
[$, E', T']       |   + 3 * 4 $ | Reduce: T' -> None
[$, E']           |   + 3 * 4 $ | Reduce: E' -> +TE'
[$, E', T, +]     |   + 3 * 4 $ | Shift
[$, E', T]        |     3 * 4 $ | Reduce: T -> FT'
[$, E', T', F]    |     3 * 4 $ | Reduce: F -> N
[$, E', T', N]    |     3 * 4 $ | Shift
[$, E', T']       |       * 4 $ | Reduce: T' -> *FT'
[$, E', T', F, *] |       * 4 $ | Shift
[$, E', T', F]    |         4 $ | Reduce: F -> N
[$, E', T', N]    |         4 $ | Shift
[$, E', T']       |           $ | Reduce: T' -> None
[$, E']           |           $ | Reduce: E' -> None
[$]               |           $ | Acc
```

### `2 * 3 + 4`

```
STACK             | INPUT       | ACTION
------------------------------------------------------------
[$, E]            | 2 * 3 + 4 $ | Reduce: E -> TE'
[$, E', T]        | 2 * 3 + 4 $ | Reduce: T -> FT'
[$, E', T', F]    | 2 * 3 + 4 $ | Reduce: F -> N
[$, E', T', N]    | 2 * 3 + 4 $ | Shift
[$, E', T']       |   * 3 + 4 $ | Reduce: T' -> *FT'
[$, E', T', F, *] |   * 3 + 4 $ | Shift
[$, E', T', F]    |     3 + 4 $ | Reduce: F -> N
[$, E', T', N]    |     3 + 4 $ | Shift
[$, E', T']       |       + 4 $ | Reduce: T' -> None
[$, E']           |       + 4 $ | Reduce: E' -> +TE'
[$, E', T, +]     |       + 4 $ | Shift
[$, E', T]        |         4 $ | Reduce: T -> FT'
[$, E', T', F]    |         4 $ | Reduce: F -> N
[$, E', T', N]    |         4 $ | Shift
[$, E', T']       |           $ | Reduce: T' -> None
[$, E']           |           $ | Reduce: E' -> None
[$]               |           $ | Acc
```
