# Language 

Parsers a written in a language called the Algodal Text Parser Generator Language (ATPGL). The language has a similar *EBNF* like syntax for defining grammar actions and a domain specific language (DSL) for complex token processing.

Here is a sample syntax for a basic parser:

```parser
name = (oneof "ABCDEFGHIJKLMOPQRSTUVWXYZ")+
number = (oneof "0123456789")+
space = (oneof " \t")+
newline = "\r\n" / "\n"

stmt = name space number space? newline*

output {
  stmt {...},
  name,
  number,
}
```

Algodal Text Parser Generator (ATPG) generates the token list and the abstract syntax tree for you based on the output configuration you specify.
