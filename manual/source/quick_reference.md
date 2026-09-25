# Quick Reference

A one-page summary of every APML feature. Each entry links to its full chapter.

## Module — [details](module.md)

```parser
program MyParser;         # name the module
program "algodal" json;   # ... in two parts; the full name is algodaljson
```

## Actions — [details](language.md)

```parser
a  = "x";   # charseq action (=)  -> flat characters
b := "x";   # syntac action (:=)  -> AST node
```

## Series, Options, Groups — [details](language.md)

```parser
s = A B C;          # series: A then B then C
o = A | B;          # option (OR): every alternative checked, longest wins
f = A / B;          # option (Firstly OR): stop at first match
g = A (B | C) D;    # group as a single unit
```

## Comments — [details](language.md)

```parser
# line comment to end of line
```

## Alias — [details](alias.md)

```parser
alias tab \x09;     # a name for a literal value
```

## Characters — [details](character.md)

```parser
A = char;        # any single utf-8 character
B = <A:Z>;       # character block; ranges use ':'
C = \x41;        # hex literal (A)
D = \u0041;     # unicode literal (A)
E = \x43,41,54;  # chain -> "CAT"
F = \x41:5A;     # range A..Z
```

## Counters — [details](counter.md)

```parser
<A:Z>+;      # one or more
<A:Z>*;      # zero or more
<A:Z>?;      # zero or one (optional)
<A:Z>-5;     # exactly 5
<A:Z>-5+;    # five or more
<A:Z>-7:12;  # between 7 and 12
```

## Built-in Actions — [details](builtin_action.md)

```parser
spc;   # space or tab
nl;    # line break
eol;   # end-of-line (a line break or end of input)
eof;   # end of input (matches zero width)
```

## Inbetween (skip) — [details](inbetween.md)

```parser
stmt = "(" . "A" . ")";  # '.' skips per the config below
. { spc, nl }            # required whenever '.' is used
```

## Stopping a counter — [details](counter.md)

```parser
char*::until("-->")   # repeat until "-->", and take it too
(char* ^ "-->")       # repeat until "-->", and leave it for the next unit
```

A counter followed by its own base needs neither — `A+ A` is compiled as
`A A+`.

## Permutation — [details](permutation.md)

```parser
A = perm["A" "B" "C"];  # match members in any order, each once
```

## Text Functions — [details](text_function.md)

```parser
tex::order("ABC");   # same length, any character order
tex::oneof("ABC");   # one character from the set
tex::icase("ABC");   # case-insensitive exact match
tex::icase(word);    # ...over a texvar, or a semvar's members
```

## Result Functions — [details](parser_result_function.md)

A **predicate** asks a question about the matched text and can only pass or fail
it. A **producer** answers with a number instead, and never fails anything.

```parser
# predicates
name::is("Fred");        # matched text equals
name::not("Amber");      # ... does not equal
name::subkind("Fr");     # ... contains

# narrowing what is asked about
name::part(1);           # 1-indexed character
name::part(1:4);         # characters 1..4
name::part(2+);          # character 2 to the end
name::part(1)::is("F");  # chained

# producers -- no parentheses, they take no argument
name::char_count;        # characters matched
name::to_num;            # matched text as a number; 0 if it is not one
A+::iter_steps;          # times a counter ran; 1 if not counted, 0 if none

# a producer may be compared against a NUMBER
name::char_count::is(3);      # exactly three characters
name::to_num::is(200);        # the value 200 -- so "0200" matches too
name::char_count::is(limit);  # ... or against a numvar

```

## Variables — [details](variable.md)

Local to one action, or global to the whole parse. A `texvar` holds a span of
text; a `numvar` holds a number.

```parser
texvar greeting = "Hello";   # global, set before parsing starts
numvar limit = 3;            # global number

A := (word => texvar x) x;   # capture, then require the same text again
B := (word => texvar x) (word => x);   # declare once, assign again
C := (n::to_num => numvar v);          # a producer fills a numvar
```

A variable must be assigned on **every** path that reaches a read, or the
grammar is refused — nothing is zeroed, so there is no safe stale value.

## Semvar — [details](variable.md)

A **set** of text the grammar builds as it parses and then matches against —
what a semantic predicate needs and a plain variable cannot give. Global, at
most four.

```parser
semvar kind = "int", "short";        # declared members
semvar name;                         # starts empty

decl := "typedef" (ident => kind) ";";   # add what was parsed
use  := kind;                            # match any member, longest first
alt  := kind::first;                     # ... earliest added instead
soon := try kind [ident] ";";            # read it before it is declared
```

`try set [unit]` matches the bracketed unit — the **replacement matcher** — and
promises that text will be declared into `set` before the input ends. A promise
still owed when the input runs out is an error. One semvar, one unit.

## Scope — [details](variable.md)

A depth the **input** moves. Leaving a scope forgets whatever was added to the
sets bound to it — ordinary block scoping.

```parser
scope blk
    begin = "{";
    end   = "}";

feat {"scope": blk} semvar kind = "int";   # bound; an unbound set never forgets

block := blk::begin item* blk::end;
```

`begin` and `end` may sit in different actions, and blocks nest freely.

Written as **lists**, the brackets pair by position — whatever opened a level is
the only thing that closes it, so `{ ... )` does not close. Two to four
positions, and the two lists must be the same length:

```parser
scope blk
    begin = ["{", "("];
    end   = ["}", ")"];
```

## Logic Blocks — [details](logic_block.md)

A logic block **tests values**. It reads no input and moves no cursor: it
succeeds or fails, and consumes nothing either way. `{{ ... }}` is *final* — it
runs for what it does, always holds, and nothing may follow it in the grammar.

```parser
A := (word => texvar x) {x == "cat"};      # a test
B := "a" {{9 => n}};                       # a deed, always holds
```

Operators, in C's precedence, tightest first:

```parser
NOT a            # negation
a * b   a / b    # division by zero is 0
a + b   a - b    # a - b clamps at 0
a < b   a <= b   a > b   a >= b
a == b  a != b   # text compares by bytes; == and != are all text has
a AND b          # short-circuits: b is not evaluated when a is false
a OR b           # short-circuits: b is not evaluated when a is true
TRUE  FALSE      # one and zero
set::is(t)  set::not(t)  set::clear    # questions about a semvar
error("...")                           # stop the whole parse
```

Statements are separated by `;`, and the last one's value is the block's answer.
A statement that produced nothing — an assignment, a cleared set — is a deed
rather than an answer, and a deed is no reason to fail.

### `error("...")`

Every other failure means *"this did not match here"*, and it sends the machine
looking for another reading. `error()` means the input is wrong and there is
nothing else to try: it travels straight out of options, series, counters,
permutations and `if` conditions alike, ends the run, and its message becomes
the run's error.

```parser
z := (word => texvar x) {x == "cat" OR error("only cats here")};
```

Because `OR` short-circuits, that reports nothing for a cat and stops for a dog.
`{{ }}` does not absorb it either — always holding is an *answer*, and `error()`
does not give one.

## IF Statements — [details](if_statement.md)

```parser
if (cond) [then | else]     # both branches
if (cond) [then]            # then only
if (cond) [| else]          # else only
```

The condition may be a logic block or a grammar; a grammar condition **consumes**
what it matched. With no branch to take, an `if` is like `E?` — the cursor
resets and the next unit is read.

## Feature Config

How a declaration is configured, written apart from what it declares. Entries
are keyed, so order never matters; a key the feature does not read is an error.

```parser
{ "key" : value , ... }     # value is a label, a number or a string
```

## Config — [details](config_settings.md)

What the grammar asks the machine to build. Optional; every setting has a
default and what you do not write keeps it.

```parser
config {
    "ast-node-text" : FALSE,     # literals stop being nodes
    "ast-node-char" : TRUE,      # char literals start being nodes
}
```

| setting | default |
|---|---|
| `ast-node-action` | `TRUE` |
| `ast-node-text` · `-text-counter` · `-text-series` | `TRUE` |
| `ast-node-char` · `-char-counter` · `-char-series` | `FALSE` |

A matched literal is a node named by **what it matched**, and adjacent literals
make **one** node — `"A" "B"` is `text "AB"`. A `.` between them ends the run, so
`"a" . "b"` stays two. Turn everything off and a parse builds no tree at all,
which is all a recogniser needs.

**Changing a setting changes the AST.** An interpreter is written against one
config.

## Parser Block — [details](parser.md)

```parser
parser {
    main_grammar;   # the single start grammar; the loop re-runs it over what remains
}
parser { A | B | C; }       # an option
parser { A B C; }           # a series
parser { item; }            # the loop walks adjacent items
parser { item (. item)*; }  # items separated by the inbetween (`.`)
```

## Node IDs — [details](abstract_syntax_tree.md)

```parser
node_id {
    Label: "saved name",    # what an action is saved as in the AST
}
```

## Linking — [details](module.md)

```parser
link p2;                    # a separate machine, called into
link "algodal" json;        # sugar for `link algodaljson;`
X := p2::value;             # always qualified
```

## Binding Power — [details](binding_power.md)

```parser
bindpow bp {
    "+" : (50, 51) ;        # r = l + 1  -> left-associative
    "^" : (11, 10) ;        # r = l - 1  -> right-associative
    "not" : (0, 70) ;       # (0, r) prefix; (l, 0) postfix
}

feat {"bind": bp} expr := atom | expr . "+" . expr | "not" . expr;
```

## Foreign Bodiess — [details](foreign.md)

```parser
indent = _;                        # body lives in your C code
foreign { indent: "apm_py_indent" }
```

## AST Maps — [details](abstract_syntax_tree.md)

```parser
(A . B) -> (B A)          # order in the map is order in the tree
(A . B) -> (A: (B))       # A becomes B's parent
(A . B) -> (A)            # B is discarded
(A . B) -> (A [B])        # B's children take B's place
(A => texvar v) -> (A node("Extra", v))    # a node nothing matched
('a'A . 'b'A) -> ('b' 'a')                 # labels tell two apart
```

## System Functions — [details](system_function.md)

```parser
error("only cats here")     # stop the parse; nothing else is tried
```

## Keywords — [details](keywords.md)

Every word the language spells out is reserved and cannot be a declared name.
Config and feature keys are quoted strings, so they are exempt.

## How to Use — [details](how_to_use.md)

```sh
apma mylang.apm -o mylang.apmb
```

```c
ApmBinary   program = ApmReadBinaryFile("mylang.apmb", &ok);
ApmVmResult result  = ApmVmRun(&program, config);
```
