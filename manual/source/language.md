# Language

Parsers are written in the **Algodal Parser Machine Language (APML)**. The
language uses an *EBNF*-like syntax for grammar rules — called **actions** —
together with extra syntax for matching characters, for deciding on context, and
for shaping the abstract syntax tree.

## The smallest parser

Two actions and a `parser` block. That is a working parser.

```parser
A = "cat";
B = "dog";
pet := A | B;

parser { pet; }
```

Over `catdog` that gives two root nodes, a `pet` for each, with the matching
action underneath.

Notice there is no `program` line. It is **optional** — a grammar that stands
alone does not need a name. You want one as soon as another module might
[link](module.md) to yours, because the name is how it is referred to.

## A slightly bigger one

```parser
# A simple parser
program greeting;

name   = <A:Z>+;
number = <0:9>+;
stmt  := name . number . eol;

parser { stmt; }

. { spc }
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

- `|` (**OR**) — every alternative is tried, and the **longest** match wins. A tie goes to the one written first.
- `/` (**Firstly OR**) — trying stops at the *first* alternative that succeeds.

So in `dog | cat`, `cat` is tried even when `dog` already matched, and whichever consumed more text is kept. In `dog / cat`, `cat` is only tried if `dog` fails.

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

APML has three types.

| Type | Keyword | Holds |
| :--- | :--- | :--- |
| **Text** | `texvar` | a sequence of characters |
| **Number** | `numvar` | `0` or a positive number; negatives and decimals are not supported |
| **Semantic** | `semvar` | a *set* of text values, matched like an option of its members |

:::{seealso}
A parse result is not a type of its own. `=>` assigns one to a variable, and
the variable's type says what is kept. See [Variables](variable.md).
:::

## Literals

Two kinds of literal appear in a grammar.

A **string-literal** is text in double quotes. It matches those characters
exactly:

```parser
A = "cat";
```

A **char-literal** names a single character by its code, in hex with `\x` or by
code point with `\u`:

```parser
B = \x41;      # A
C = Ω;    # Greek capital omega
```

:::{important}
APM reads **UTF-8**, and a hex literal must be valid UTF-8. `\x41` is the
single byte `A`, which is fine. A lone `\xC3` is not — it is the first byte of
a two-byte sequence and means nothing on its own.

For anything above 127, `\u` is the safer way to say it: give the code point
and let the compiler write the bytes.
:::

## Char-Range

A **char-range** parses a single character out of a span of codes. It is
written with `:`, and it is what goes inside a
[character block](character.md):

```parser
D = <A:Z>;        # one character, A through Z
E = \x41:5A;      # the same, by code
```

A char-range matches **one** character. That is what separates it from a
[counter](counter.md), which also uses `:` — a counter's `:` bounds how many
times something runs, a char-range's says which characters are allowed.

The same `:` sections a result in
[`::part(1:4)`](parser_result_function.md).

## Reserved Words

Every word the language spells out is **reserved**: it cannot be the name of an
action, a variable, or anything else you declare. The list is short — see
[Keywords](keywords.md).

## A Note on "Text"

The word *text* can mean two things. **Incoming text** (also known as a buffer)
is the content being parsed into an AST. **Parsing text** (also known as a
string-literal, a texval, or just text) is any grammar or parameter you write
in APML. The context makes clear which one is meant.
