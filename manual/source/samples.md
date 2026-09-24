# Samples

Four complete parsers, from the smallest useful thing to a tour of the whole
language. Every grammar on this page compiles as written.

## A line-oriented language

```
A 100
B  25
```

```parser
# A line-oriented language:  A 100
program basic;

name   = <A:Z>+;
number = <0:9>+;

entry := (name . number) -> (name: (number));

parser { . entry . ; }

. { spc, nl }
```

Each line becomes an `entry`, with the number placed **under** the name by the
AST map rather than beside it:

```
entry "A 100"
└── name "A"
    └── number "100"
entry "B  25"
└── name "B"
    └── number "25"
```

The parser block holds one start grammar, and the loop re-runs it over what is
left — which is why a file of many lines needs no counter. The `.` around it is
what lets the newline between entries be skipped.

## An expression language

```
X = 23 + 5 * (6 - 4)
```

Precedence is not something the grammar shape can carry, so it goes in a
[binding power](binding_power.md) table and the rule is bound to it.

```parser
# An expression language with precedence:  X = 23 + 5 * (6 - 4)
program expression;

name   = <A:Za:z> . (<A:Za:z_0:9>)*;
number = <0> | <1:9> . <0:9>*;

bindpow bp {
    "+" : (50, 51) ;
    "-" : (50, 51) ;
    "*" : (60, 61) ;
    "/" : (60, 61) ;
    "^" : (71, 70) ;
}

feat {"bind": bp} expr := atom
    | expr . "+" . expr
    | expr . "-" . expr
    | expr . "*" . expr
    | expr . "/" . expr
    | expr . "^" . expr
    ;

atom  := number | name | group;
group := ("(" . expr . ")") -> (expr);

assign := (name . "=" . expr) -> (name: (expr));

parser { . (assign | expr) . ; }

. { spc, nl }
```

Note what the map on `group` does: `-> (expr)` keeps `expr` and drops the two
bracket literals, so the parentheses do their job and then get out of the way.

The result groups the way arithmetic says, not the way recursion fell:

```
assign "X = 23 + 5 * (6 - 4)"
└── name "X "
    └── expr "23 + 5 * (6 - 4)"
        ├── atom → number "23"
        ├── text "+"
        └── expr "5 * (6 - 4)"
            ├── atom → number "5 "
            ├── text "*"
            └── atom → group → expr "6 - 4"
```

## Indentation, in C

```
X:
  Y
  Z
```

What counts as an indent depends on a stack of earlier indents, which is not a
shape any grammar can state. So those three actions have **no body**, and your
program supplies them — see [Foreign Bodies](foreign.md).

```parser
# Indentation, which no grammar can describe: the body lives in C.
program pylike;

name = <A:Za:z> . (<A:Za:z_0:9>)*;

indent  = _;
dedent  = _;
newline = _;

block := name . ":" . indent . (name . newline)* . dedent;

foreign {
    indent:  "apm_py_indent",
    dedent:  "apm_py_dedent",
    newline: "apm_py_newline",
}

parser { . block . ; }

. { spc }
```

## A tour of the rest

Variables, a set the grammar learns as it goes, a scope those members are
forgotten at, logic, a branch, order-free members, and a config change.

```parser
# A tour: variables, a learned set, scopes, logic, if, perm and config.
program tour;

config { "ast-node-text" : FALSE };

alias q  \x22;
alias max 8;

digit = <0:9>;
alpha = <a:zA:Z>;
ident = (alpha | "_") . (alpha | digit | "_")*;
num   = digit+;

numvar limit  = 8;
texvar banner = "tour";

scope blk
    begin = "{";
    end   = "}";

# bound to blk, so leaving the block forgets what was declared inside it
feat {"scope": blk} semvar declared;

# capture, then require the same text again
repeat := (ident => texvar w) . "=" . (ident => w);

# a producer into a numvar, then a test over it
short  := (num::char_count => numvar n) . {n < limit};

# add to the set as it parses, then match any member
declare := "var" . (ident => declared) . ";";
use     := declared;

# a bounded counter, and a run of characters checked one at a time
field   := alpha-1:max;
quoted  := q . char::not(q)* . q;

# order-free members, each separated by the skip
attrs   := perm[(ident .) (num .)];

# branch on whether something parses
maybe   := ident . if (num) ["!" | "?"];

body    := blk::begin . (declare | use | repeat)* . blk::end;

parser { . (body | short | field | quoted | attrs | maybe) . ; }

. { spc, nl }
```

Worth picking out:

- `(ident => texvar w) . "=" . (ident => w)` captures text and then **requires
  the same text again**. This is the thing a plain grammar cannot do.
- `declared` is a [semvar](variable.md): `(ident => declared)` adds to the set
  as the parse goes, and writing `declared` afterwards matches any member.
- `blk::begin` and `blk::end` move a depth, and leaving the block forgets what
  was declared inside it. That forgetting is the whole point of a scope, so a
  scope with no semvar bound to it is refused rather than silently doing
  nothing.
- `char::not(q)*` puts the counter **after** the chain, so the question is
  asked of each character. Written `char*::not(q)` it would ask once, of the
  whole run against a single quote.
- `alpha-1:max` takes a bound from an [alias](alias.md), so the limit is named
  in one place.

## What ships in `assets/samples`

Each one is a grammar somebody can copy, and the checks compile all of them and
parse each one's `.txt` on every build.

| | |
| :--- | :--- |
| `json.apm` | the smallest complete language |
| `ini.apm` | no standard exists, so it follows the three readers that matter; a line-oriented inbetween |
| `xml.apm` | the W3C grammar, with a tree shaped by maps |
| `yaml.apm` | indentation without a foreign body, by staying line-oriented |
| `html.apm` | hands `<script>` bodies to `javascript.apm` with `link` |
| `javascript.apm` | a precedence table, left recursion, and folds |
| `c.apm` + `cpp.apm` | two linked programs: the language, and the preprocessor that is not it |
| `python.apm` | indentation in C (`python_foreign.c`), soft keywords with a semvar |
| `haskell.apm` | operators and layout kept to one line |
| `decree.apm` | a small domain language, end to end |
| `expr.apm` | left recursion and the optimizer's worst case, deliberately without precedence |
| `expr_bindpow.apm` | the same grammar with a table: precedence, but the operator is still a sibling |
| `expr_bindpow_astmap.apm` | and with a map: the operator becomes the parent |
| `plain.apm`, `min.apm`, `dev.apm` | the smallest things that are still parsers |

The three `expr` files read the same input, so the difference between them is
the difference a table makes and then the difference a map makes.

:::{seealso}
[Quick Reference](quick_reference.md) has every feature on one page.
:::
