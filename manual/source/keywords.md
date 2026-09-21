# Keywords

Every word APML spells out, in one place.

All of them are **reserved**. A keyword cannot be the name of an action, an
alias, a variable, a semvar, a scope, a binding-power table, a linked module or
a capture label.

```parser
node_id = "x";   # refused: 'node_id' is a reserved word
node_ident = "x";  # fine -- containing a keyword is not being one
```

## The list

| | |
| :--- | :--- |
| **Declarations** | `alias` `bindpow` `config` `custom_action` `link` `node_id` `parser` `program` `scope` `semvar` |
| **Variable types** | `numval` `texval` |
| **Built-in actions** | `eof` `eol` `nl` `spc` |
| **Units and control** | `char` `error` `if` `node` `perm` |
| **Text functions** | `icase` `oneof` `order` |
| **Result functions** | `begin` `char_count` `end` `first` `is` `iter_steps` `not` `part` `per` `subkind` `to_num` |
| **Scope and semvar bodies** | `clear` `feat` |

## What is *not* reserved

**Config and feature keys.** They are written as quoted strings, and that is
exactly what keeps them out of the way of names:

```parser
config { "ast-node-text" : FALSE };
semvar kind {"scope": blk} = "int";
bindpow bp { "and" : (20, 21) ; };
```

A string can never be mistaken for an identifier, so `"begin"` as a key and
`begin` as a result function never meet.

**`TRUE` and `FALSE`.** They are config values, not keywords.

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
