# Operator Precedence Parser

## Description

The implementation is similar to LR(0) parser, but the reducing rule is much straightforward:
- `N`umber > Everything
- `$`(ending symbol) < Everything
- `+` and `-` < `*` and `/`
- When the precedence is same, such as `+` meets `+` or `-`, then reducing
- When meeting `$`(ending symbol), then return the result

Check [the video](https://www.youtube.com/watch?v=n5UWAaw_byw&list=PLEbnTDJUr_IcPtUXFy2b1sGRPsLFMghhS&index=9) and [wiki](https://en.wikipedia.org/wiki/Operator-precedence_parser) for details.

## Grammar
```
E -> E+E
E -> E-E
E -> E*E
E -> E/E
E -> N
```

## Operator Precedence
```
 ε | N | + | - | * | / | $
---+---+---+---+---+---+---
 N | ε | > | > | > | > | >
---+---+---+---+---+---+---
 + | < | > | > | < | < | >
---+---+---+---+---+---+---
 - | < | > | > | < | < | >
---+---+---+---+---+---+---
 * | < | > | > | > | > | >
---+---+---+---+---+---+---
 / | < | > | > | > | > | >
---+---+---+---+---+---+---
 $ | < | < | < | < | < | ε
```

## Example:  `3 + 2 * 2`
```
# Example:  3 + 2 * 2
STACK        | SYMBOLS   | INPUT       | ACTION
------------------------------------------------------------
[$]          |           | 3 + 2 * 2 $ | shift ($ < N)
[$, N]       | 3         |   + 2 * 2 $ | reduce E -> N
[$]          | 3         |   + 2 * 2 $ | shift ($ < +)
[$, +]       | 3 +       |     2 * 2 $ | shift (+ < N)
[$, +, N]    | 3 + 2     |       * 2 $ | reduce E -> N
[$, +]       | 3 + 2     |       * 2 $ | shift (+ < *)
[$, +, *]    | 3 + 2 *   |         2 $ | shift (* < N)
[$, +, *, N] | 3 + 2 * 2 |           $ | reduce E -> N
[$, +, *]    | 3 + 2 * 2 |           $ | reduce E -> E * E
[$, +]       | 3 + 4     |           $ | reduce E -> E + E
[$]          | 7         |           $ | Done
```
