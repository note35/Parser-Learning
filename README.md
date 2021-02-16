# Parser-Learning

This repository contains many of my parser Implementation for LeetCode problem [227. Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/). I also posted the same content into leetcode discussion, you can check the post there directly.

## Why should I learn parser?

A way to dive deep into the details of [PEP617](https://www.python.org/dev/peps/pep-0617/) is to get your hands dirty. And leetcode is one of the best online judges to verify the implementation.

### Resource to learn Compiler

If you are like me before without a background in language parsing, here is the resource I used.

- [Uncode - GATE Computer Science: Compiler Design lecture](https://www.youtube.com/watch?v=Qkwj65l_96I&list=PLEbnTDJUr_IcPtUXFy2b1sGRPsLFMghhS): This channel covers LL(1), LR(0), SLR(1), LR(1), CLR(1), LALR(1), and Operator Precedence parser.
- [Packrat Parsing: Simple, Powerful, Lazy, Linear Time by Bryan Ford](https://pdos.lcs.mit.edu/~baford/packrat/icfp02/): The website of Bryan Ford, author of Packrat parser, provides the paper with implementation details and haskell implementation.

### Why do I pick [227. Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/)?

Firstly, Leetcode contains many parsing related questions, **227. Basic Calculator II** is one of the simplest one with just enough constraints for learning, which only requires to handle 5 type of symbols: + - * / and number, and all the input strings are valid.

Secondly, before I started my study, there were only LL(1) parser and Operator Precedence parser posts in discussion, LR(0), and Packrat parser were missing. Even if you search the related simple implementation in Google or other search engines, there's actually no organized work like this. (Implement all sorts of parsers for the same problem.)

## TODO(?)

- [Low] Implement Operator Precedence parser (There're already examples from others in LeetCode discussion.)
- [Low] Convert Packrat parser to PEG parser (This may be overkill for just five symbols grammar.)
