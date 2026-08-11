# Language 

Parsers are written in a language called the **Algodal Parser Machine Language (APML)**. The language uses an *EBNF*-like syntax for defining grammar actions (simply called *actions*). It also has special syntaxes for defining lexers and analyzers, and for generating a token list and an abstract syntax tree.

Here is a sample syntax for a basic parser:

```parser
# A simple parse
name = tex::oneof("ABCDEFGHIJKLMOPQRSTUVWXYZ")+;
number = tex::oneof("0123456789")+;
space = tex::oneof(" \t")+;
newline = "\r\n" / "\n";
stmt := name space number space? newline*;

parser { stmt }
```


## Comment

You can create line comments with `#` symbol.

```parser
# Hello
# I am a comment
```

## Action

An action is the definition of a parsing action. Actions parse blocks of character sequences (charseq for short) and structures of syntactic nodes (syntac for short) which are like an AST. A charseq action is defined using `=` while a syntac action is defined using `:=`. It is the same grammar regardless of it being a charseq or syntac grammar - the only difference is that one results in a block of character sequence while the other results structured tree.

In below example, we defined an action called animal and it parses for an exact match for the string *"cat"*.

```parser
animal_simple  = "cat" # charseq
animal_detail := "c" "a" "t" # syntac
```

In the next example, we defined 3 actions: dog parsers for exactly "dog", cat parses for exactly "cat" and animal parses for actions *dog* followed by *cat* which is equivalent to *`animal = "dog" "cat"`*.

```parser
dog     = "dog"
cat     = "cat"
animal := dog cat
```

In this example, it is similar to the previous example except that animal parses for the action *dog* *OR* the action *cat*.

```parser
dog     = "dog"
cat     = "cat"
animal := dog | cat
```

This example is the same except animal parses for the action *dog* *OR* the action *cat* *whichever first*.

```parser
dog     = "dog"
cat     = "cat"
animal := dog / cat
```

The difference between the last 2 examples is `|` (*OR*) and `/` (*Firstly OR*). With *OR*, every case is checked regardless of whether an earlier one succeeded. With *Firstly OR*, checking stops at the *first* successful case. So in `animal := dog | cat`, even if `dog` parses the text successfully, the parser still checks `cat`. In `animal := dog / cat`, `cat` is only checked if `dog` fails to parse.

:::{tip}
Reach for `/` (*Firstly OR*) when the order of alternatives matters or you want to stop at the first match — it is usually what you want and avoids redundant checks. Use `|` (*OR*) when every alternative must be considered.
:::

An action can be considered to be containing *series* and *options*.

```parser
act = A B C
```

`A B C` are actions that are parsed in that order: A followed by B followed by C. This is called a *series*. Each member of a series is generally called a *unit*.

```parser
act = D | E
```

`D | E` are actions that are parsed in *parallel*. This is called an *option*. Even if the parser goes through all *options* only one *option* can be *move* the parsing progress. If we had `D / E` instead (also an option), we stop checking other possible options once we find the first successful parse.

```parser
act = A B C | D 
```

Options are lists of series. Therefore in the case `A B C | D` the parser will see an *option* of series `A B C` *OR* series `D`.

```parser
act = A B C | D E | F G H
```

So `A B C | D E | F G H` is an option of 3 series: `A B C` *OR* `D E` *OR* `F G H`.

If we wanted to change how the parser interpret the series and options we can use *groups*. Groups can be defined anywhere and it is defined using curved-brackets `()`.

```parser
act = A B (C | D) E | F G H
```

Because of the group `(C | D)`, at the level of `act` action we have an option of 2 series. `(C | D)` is interpret as a *unit* in the series `A B (C | D) E`. The second series is `F G H`. If we zoom in into the unit `(C | D)` it is a group of an option of 2 series `C` and `D`.

A group can go anywhere:

```parser
act = (A B (C | D) E | F (G) H)
```

## Character Sequence

A character sequence is a block of sequential characters parsed from an incoming text. It is generated in the lexing phase and is the building block of the Abstract Syntax Tree (AST). A character sequence that is saved in an AST is also known as a token.

Actions that generate charseq are defined with `=`.

```parser
number = <0:9>+;
```

## Syntactic Object
A syntactic object or syntactic node or abstract syntax tree node is either a charseq or a syntac (reversive in nature) in an AST tree.

Actions that generate syntac are defined with `:=`.

```parser
prog := "A" number;
```

## Types

There are 4 types in APML: **Text type**, **Number type**, **Parser type** and **Semantic Type**.

Text type holds text - a sequence of characters.

Number type is 0 or positive numbers; negative numbers are not supported.

Parser type holds the result of the parsing. It can be automatically converted to Text type or Number type.

Semantic type is a special operating type that holds a **set** of parser types. That set can be applied like an **option** of text matches in grammar.


:::{seealso}
Each of these types has a corresponding variable keyword (`parval`, `numval`, `texval`). See [Variables](variable.md).
:::

## Text

When we say "text" we may be referring to a text used for parsing or an incoming text. Incoming text is the actual content that we are parsing to convert into AST. The parsing text is any grammar or parameters we used.



:::{seealso}
The semantic type is used through the `semval` variable keyword. See [Variables](variable.md).
:::

## Range

Range is a special subfeature used within other features. It specifies a starting position and an ending position, and applies an effect across the entire range. It uses the symbol `:`. More on ranges in later chapters.

:::{seealso}
Range appears in [Character](character.md) literals and blocks, [Counter](counter.md) repetitions, and [Parser Result Function](parser_result_function.md) sectioning with `::part`.
:::
