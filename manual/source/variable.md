# Variables

A variable keeps something a rule already matched, so a later part of the
grammar can use it again. This is what turns a grammar from a shape into a
grammar that can *check* things.

There are two variable types and one set type:

| Keyword | Holds |
| :--- | :--- |
| `texvar` | a span of text |
| `numvar` | a number, `0` upward — no negatives, no decimals |
| `semvar` | a **set** of text the grammar builds and later matches against |

## Capturing with `=>`

Inside an action, `(unit => target)` runs the unit and keeps what it matched.
The target is either a new declaration or a variable already in hand:

```parser
A := (word => texvar x) x;             # capture, then require the same text again
B := (word => texvar x) (word => x);   # declare once, assign again
C := (n::to_num => numvar v);          # a producer fills a numvar
```

A variable must be assigned on **every** path that reaches a read, or the
grammar is refused. Nothing is zeroed, so there is no safe stale value to fall
back on.

An alternative that assigns and then loses is rolled back. Only the winning
alternative's assignments survive a choice.

## Globals

A global is declared at the top level and lives for the whole parse. It must be
given an initial value:

```parser
texvar greeting = "Hello World";
numvar limit = 50;
```

The initial value is set once, before any input is read — so writing `greeting`
in a grammar matches that text until something assigns over it.

## Local scope

A variable declared inside an action belongs to that action, and to **one entry
into it**. Calling the action again, recursion included, gives the new
activation its own copy, so an outer value is never disturbed by an inner one:

```parser
w = <a:z>;
rec := (w => texvar x) rec? x;   # an even-length palindrome
```

## Semvar — a set the grammar learns

A `semvar` is a set of text that the parse **adds to** and later matches
against. It is what a semantic predicate needs and a plain variable cannot
give: a grammar that knows which identifiers have been declared.

Sets are global, and there are at most sixteen of them.

```parser
semvar kind = "int", "short";   # with members from the start
semvar name;                    # starting empty

decl := "typedef" . (ident => kind) . ";";   # add what was parsed
use  := kind;                                # match any member, longest first
alt  := kind::first;                         # ... earliest added instead
```

Writing the set's name **matches** any member, taking the longest. `::first`
takes the earliest added instead.

## Scope — a depth the input moves

A `scope` is a depth counter that the **input** moves. Leaving a scope forgets
whatever was added inside it to the sets bound to that scope. Ordinary block
scoping, in other words.

At most sixteen, the same ceiling as the sets.

```parser
scope blk
    begin = "{";
    end   = "}";

feat {"scope": blk} semvar kind = "int";   # bound to blk

block := blk::begin . item* . blk::end;
```

`feat { ... }` goes in **front** of the thing it configures, the same place it
goes in front of an action that binds a precedence table. What the keys mean is
not shared: an action reads `"bind"`, a semvar reads `"scope"`.

`blk::begin` runs the begin grammar and, if it matches, goes one level deeper.
`blk::end` comes back out and empties every set bound to `blk` of whatever was
added inside. A set that is not bound to a scope never forgets.

`begin` and `end` may sit in different actions, and blocks nest freely.

A `begin` or `end` value is grammar like any other: it may name an action, and
that action counts as used.

`blk::begin` and `blk::end` go **anywhere an action goes** — inside a counter,
a choice, a permutation, a result function, and as a
[binding power](binding_power.md) key when the scope's value is one fixed text.
The [skip](inbetween.md) is the one place with a condition: there the value has
to be static or known, because the skip runs at every `.` and what it opens or
closes should be something a reader of the grammar can see.

### A scope on its own

A scope needs no set. Without one it is still a depth counter, and a
positioned one still pairs its
brackets — which is sometimes all a grammar wants. One rule for a quoted
string, instead of one alternative per quote:

```parser
scope q
    begin = ["'", "\""];
    end   = ["'", "\""];

content = char::not(<'">)*;
str := q::begin content q::end;      # 'ab' and "ab", never 'ab"
```

What a scope does need is to be **used**. A scope that no `name::begin` or
`name::end` mentions is warned about (`W-unused-scope`). One of the two is
enough, because the other may be written in a grammar that
[links](module.md) this one. A scope left unused here on purpose says so with
`feat {"unused-ignore": TRUE}` — see
[Unused on purpose](language.md).

### Several brackets, paired by position

Written as a **list**, the two sides pair up position by position: whatever
opened a level is the only thing that closes it.

```parser
scope blk
    begin = ["{", "("];
    end   = ["}", ")"];
```

`{ ... }` and `( ... )` both open and close a level, and `{ ... )` does not
close at all. Written as a choice instead — `begin = "{" | "(";` — the pairing
is gone and `{ )` closes, which is the whole difference the list makes.

Two to seven positions, and the two lists must be the same length. A one-item
list is the ordinary scope written the long way, and compiles to the same
bytes.

**The longest opener is tried first.** `begin` takes the first opener that
matches, and the compiler puts them longest-first, whatever order they were
written in — so `["<", "<<"]` opens with `<<` when the input has it. Each
closer moves with its opener, so the pairing the list wrote is kept.

For that to be possible, the openers of a positioned scope have to be
[static or known](language.md) — strings, character literals,
character blocks, or actions made only of those. One decided while parsing is
an error (`E-scope-opener`). So are two openers of the same length that can
match the same text, like `"q"` and `<a:z>`, because no order tells them apart
(`E-scope-overlap`).

Only `begin` is held to this. `end` never chooses — it runs the closer of
whatever opened the level — and a scope with **one** position has nothing to
choose between, so its `begin` and `end` may be anything, a
[foreign](foreign.md) function included:

```parser
indent = _;
dedent = _;
scope pyblk begin = indent; end = dedent;
```

Each open level costs one byte, so how deep a scope may nest is how many bytes
it was given — 64 by default, and
[`scope-ordered-buffer-size`](config_settings.md) sets it.

## `try` — a name read before it is declared

A semvar only matches what has already been added, which is why C has forward
declarations. In a language where every declaration in a file is visible to
every other, the grammar has to read a name on trust:

```parser
semvar type;

decl := "type" . (ident => type) . ";";
use  := try type [ident] . ";";
```

`try type [ident]` matches an ordinary `ident` and writes down a **promise**:
that text will be declared into `type` before the input ends. A later
`=> type` of the same text keeps it. What is still owed when the input runs
out is an error, and so is a name that was declared into some other set.

The bare name is the **set**. The bracketed unit is the **replacement
matcher** — what runs in place of the set, matching exactly what it would have
matched on its own. One of each, and only a semvar may be named.

:::{warning}
`try` **classifies, it does not restructure.** It works when both readings are
the same tree and differ only in what the name in it is called. `T * x;` and
`a * b;` are two different trees, and a promise cannot retract a shape that is
already built.
:::

:::{seealso}
Logic blocks read these values — see [Logic Block](logic_block.md) — and an
[IF statement](if_statement.md) branches on them. `texvar`, `numvar`, `semvar`
and `scope` are [reserved words](keywords.md), as are `begin`, `end`, `first`
and `clear`.
:::
