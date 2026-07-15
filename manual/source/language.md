# Language 

Parsers a written in a language called the Algodal Text Parser Generator Language (ATPGL). The language has a similar *EBNF* like syntax for defining grammar actions (simply called actions). It also has special syntaxes for defining lexers, analyzers and generating a token list and abstract syntax tree.

Here is a sample syntax for a basic parser:

```parser
name = (oneof "ABCDEFGHIJKLMOPQRSTUVWXYZ")+;
number = (oneof "0123456789")+;
space = (oneof " \t")+;
newline = "\r\n" / "\n";
stmt = name space number space? newline*;
"BEGIN";
```

Actions are simple labels (being assigned grammar) or literal strings which are terminated by a semicolon `;`.

Algodal Text Parser Generator (ATPG) generates the token list and the abstract syntax tree if you define it.

## Comment

You can create line comments with `#` symbol.

```parser
# Hello
# I am a comment
```
