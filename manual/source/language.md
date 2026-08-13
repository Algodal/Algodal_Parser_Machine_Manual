# Language

Parsers are written in the **Algodal Parser Machine Language (APML)**. The language uses an *EBNF*-like syntax for defining grammar rules (called *actions*), together with special syntaxes for lexing, analysis, and for generating a token list and an abstract syntax tree.

Here is a small but complete parser:

```parser
# A simple parser
name = tex::oneof("ABCDEFGHIJKLMOPQRSTUVWXYZ")+;
number = tex::oneof("0123456789")+;
space = tex::oneof(" \t")+;
newline = "\r\n" / "\n";
stmt := name space number space? newline*;

parser { stmt }
```

The rest of this page covers the core building blocks. Individual features each have their own chapter.

## Comments

Line comments start with `#` and run to the end of the line.

```parser
# Hello
# I am a comment
```

## Actions

An **action** is a named parsing rule. Actions parse two kinds of things:

- a **character sequence** (*charseq*) — a flat block of characters, and
- a **syntactic node** (*syntac*) — a structured, tree-like node in the AST.

The grammar you write is identical either way; only the definition operator differs:

| Operator | Produces | Meaning |
| :--- | :--- | :--- |
| `=` | charseq | a block of characters |
| `:=` | syntac | a structured tree node |

```parser
animal_simple  = "c" "a" "t"; # charseq — flat "cat"
animal_detail := "c" "a" "t"; # syntac — structured node
```

An action's body refers to other actions by name. Here `animal` matches `dog` followed by `cat`:

```parser
dog     = "dog";
cat     = "cat";
animal := dog cat;
```

## Series and Options

An action body is made of *series* and *options*.

A **series** is a sequence of units parsed one after another, in order. Each member of a series is a *unit*.

```parser
act = A B C; # parse A, then B, then C
```

An **option** offers alternatives with `|` or `/`. Only one alternative can advance the parse.

```parser
act = D | E; # parse D or E
```

Options are lists of series, so alternatives can each be a full series:

```parser
act = A B C | D E | F G H; # three alternative series
```

### `|` versus `/`

Both `|` and `/` are options, but they differ in how alternatives are checked:

- `|` (**OR**) — every alternative is checked, even after one succeeds.
- `/` (**Firstly OR**) — checking stops at the *first* alternative that succeeds.

So in `dog | cat`, `cat` is checked even when `dog` already matched. In `dog / cat`, `cat` is only checked if `dog` fails.

:::{tip}
Reach for `/` (*Firstly OR*) when the order of alternatives matters or you want to stop at the first match — it is usually what you want and avoids redundant checks. Use `|` (*OR*) when every alternative must be considered.
:::

## Groups

Use parentheses `()` to group grammar and control how series and options nest. A group acts as a single unit within its surrounding series.

```parser
act = A B (C | D) E | F G H;
```

At the top level this is an option of two series: `A B (C | D) E` and `F G H`. Inside the first series, the unit `(C | D)` is itself an option of `C` or `D`.

Groups can be nested anywhere:

```parser
act = (A B (C | D) E | F (G) H);
```

## Types

APML has four types.

| Type | Holds |
| :--- | :--- |
| **Text** | a sequence of characters |
| **Number** | `0` or a positive number (negatives are not supported) |
| **Parser** | the result of a parse; auto-converts to Text or Number |
| **Semantic** | a *set* of Parser values, usable like an option of text matches |

:::{seealso}
Each type has a corresponding variable keyword — `texval`, `numval`, `parval`, and `semval`. See [Variables](variable.md).
:::

## Range

A **range** specifies a start position and an end position and applies an effect across that span. It is written with `:`.

```parser
D = \x41:5A; # characters A through Z
```

Ranges appear throughout the language, in [Character](character.md) literals and blocks, [Counter](counter.md) repetitions, and [Parser Result Function](parser_result_function.md) sectioning with `::part`.

## A Note on "Text"

The word *text* can mean two things. **Incoming text** is the content being parsed into an AST. **Parsing text** is any grammar or parameter you write in APML. The context makes clear which one is meant.
