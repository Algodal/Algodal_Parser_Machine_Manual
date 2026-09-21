# Keywords

Every word APML spells out, grouped by what it is for.

All of them are **reserved**. A keyword cannot be the name of an action, an
alias, a variable, a semvar, a scope, a binding-power table, a linked module or
a capture label.

```parser
node_id = "x";     # refused: 'node_id' is a reserved word
node_ident = "x";  # fine -- containing a keyword is not being one
```

## Module & Parsers

| | |
| :--- | :--- |
| `program` | names this module |
| `link` | calls into another module |

## Entry Point

| | |
| :--- | :--- |
| `parser` | the block holding the start grammar |

## Primitive

| | |
| :--- | :--- |
| `char` | one character, whatever it is |

## Built-in Functions

| | |
| :--- | :--- |
| `spc` `nl` `eol` `eof` | space, line break, end of line, end of input |

## Configuration

| | |
| :--- | :--- |
| `config` | settings for the whole grammar |
| `feat` | settings for one declaration |

## Variable

| | |
| :--- | :--- |
| `texvar` `numvar` | declare a text or number variable |

## Semantic Predicate

| | |
| :--- | :--- |
| `semvar` | a set the grammar builds and matches against |
| `clear` | empty a set |
| `scope` | a depth the input moves |
| `begin` `end` | a scope's two edges |

## Abstract Syntax Tree

| | |
| :--- | :--- |
| `node` | a node nothing matched |
| `node_id` | rename what an action is saved as |

## Text Functions

| | |
| :--- | :--- |
| `tex` | the namespace they live under |
| `order` `oneof` `icase` | any order, one of, ignoring case |

## Result Functions

| | |
| :--- | :--- |
| `is` `not` `subkind` | equals, does not equal, contains |
| `part` | narrow to a section of what matched |
| `char_count` `to_num` `iter_steps` | characters, value, repetitions |
| `first` | the earliest member of a semvar |

## System Functions

| | |
| :--- | :--- |
| `error` | stop the whole parse |

## Logic

| | |
| :--- | :--- |
| `AND` `OR` `NOT` | the operators, written as words |

## Values

| | |
| :--- | :--- |
| `TRUE` `FALSE` | one and zero |

## Units & Control

| | |
| :--- | :--- |
| `perm` | members in any order |
| `if` | branch on a test or on whether something parses |
| `alias` | a name for a literal value |
| `bindpow` | an operator precedence table |
| `custom_action` | bind a bodiless action to your C code |

:::{note}
Nothing *forces* reservation. APM is scannerless, so `perm` only reads as a
keyword before a `[`, and the parser could tell the two uses apart perfectly
well. It is reserved because the reader is not a parser — a grammar in which
`part` is sometimes a result function and sometimes a rule is one nobody can
skim.
:::

:::{seealso}
The original APG used `@<name>` commands precisely to avoid reserved words.
APM took the opposite trade: familiar keywords, and a short list of names you
cannot use. See [Overview](overview.md).
:::
