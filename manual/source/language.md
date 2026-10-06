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

parser { pet; };
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

parser { stmt; };

. { spc };
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

### Unused on purpose

An action nothing calls is warned about (`W-unused`). Sometimes that is the
point: a grammar that is [linked](module.md) by another one defines actions for
*that* grammar to call, and in its own file they are never used. Say so in
front of the definition, and the warning goes away:

```parser
feat {"unused-ignore": TRUE} directive := "#" . ident . line;
```

The same key works on a [scope](variable.md). Marking
something that **is** used is warned about too (`W-unused-ignore-used`) — the
mark says one thing and the grammar another, so one of them is out of date.
The value is a switch, `TRUE` or `FALSE`.

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

## Escapes

Inside a string-literal and inside a [character block](character.md), a
backslash starts an **escape**:

| escape | means |
| :--- | :--- |
| `\n` `\r` `\t` | newline, carriage return, tab |
| `\\` `\'` `\"` `\?` | the character itself |
| `\xHH..\e` | one character, by its UTF-8 bytes |
| `\uHHHH..\e` | one character, by its code point |

**Every keyboard symbol escapes to itself**, so a reader need not remember
which ones are special:

```
\` \~ \! \@ \# \$ \% \^ \& \* \( \) \- \_ \= \+
\[ \] \{ \} \| \; \: \, \. \< \> \/
```

```parser
open  = "\[";        # the same as "["
gt    = <\>>;        # a block holding ">" -- the easy way to get one in
```

**Letters and digits are reserved.** `\q` or `\5` is an error, not the
character, so that a later version can give one a meaning without changing
what an existing grammar says. A space and any non-ASCII character are not
escapes either.

The `\e` ends a code, and inside a string or a character block it is
required: the digits are greedy, so `"\x41\eBC"` is `ABC` while `"\x41BC"` is
an error — it would otherwise read `41BC` as one code. The same goes for
`<\x09\e >`, a tab or a space. A character literal written on its own needs
none: `\x41` ends where the grammar around it says it does.

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

## Kinds of unit

A **unit** is one step of a grammar: what a series is
a run of. The words below come up wherever the manual says what may go where.

| term | what it is |
| :--- | :--- |
| **string-literal** | text in quotes: `"cat"` |
| **char-literal** | a character by code: `\x41`, a chain `\x43,41,54`, a range `\x41:5A` |
| **char-block** | one character from a set: `<A:Z_>` |
| **group unit** | a grammar in parentheses: `("a" \| "b")` |
| **action unit** | the name of an action, which runs its body |
| **entry unit** | one entry of a list a declaration holds — a [scope](variable.md)'s opener, a [bindpow](binding_power.md) key |
| **trailing unit** | the terminator of [`::until` and `^`](counter.md) |

Every unit is also one of three **kinds**, by how much the grammar alone can
say about what it matches:

| kind | known when | matches | examples |
| :--- | :--- | :--- | :--- |
| **static** | the grammar compiles | exactly one text | `"<="`, `\x2B`, `<+>`, `"<" "="`, an action whose body is static |
| **known** | the grammar compiles | a fixed number of characters, each from a set | `<[{(>`, `tex::oneof("ab")`, `tex::icase("if")`, `<ab> "x"` |
| **dynamic** | the input is read | anything else | `"a" \| "bb"`, `"a"+`, `"a" . "b"`, `char`, `nl`, a variable, a foreign `_` |

A series of statics is static: `"<" "="` spells `<=`. A series with a `.` in
it is dynamic, because the skip decides how much lies between.

Where the kind matters:

- a [bindpow](binding_power.md) key must be **static** — it names one operator;
- a [positioned scope](variable.md)'s
  openers must be **static or known** — they are told apart by length and by
  what they match;
- a trailing unit may be **any** kind — it is simply run at each step.

## Reserved Words

Every word the language spells out is **reserved**: it cannot be the name of an
action, a variable, or anything else you declare. The list is short — see
[Keywords](keywords.md).

## A Note on "Text"

The word *text* can mean two things. **Incoming text** (also known as a buffer)
is the content being parsed into an AST. **Parsing text** (also known as a
string-literal, a texval, or just text) is any grammar or parameter you write
in APML. The context makes clear which one is meant.
