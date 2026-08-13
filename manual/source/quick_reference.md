# Quick Reference

A one-page summary of every APML feature. Each entry links to its full chapter.

## Module — [details](module.md)

```parser
program MyParser;   # name the module
link other;         # reuse another module's actions
```

## Actions — [details](language.md)

```parser
a  = "x";   # charseq action (=)  -> flat characters
b := "x";   # syntac action (:=)  -> AST node
```

## Series, Options, Groups — [details](language.md)

```parser
s = A B C;          # series: A then B then C
o = A | B;          # option (OR): every alternative checked
f = A / B;          # option (Firstly OR): stop at first match
g = A (B | C) D;    # group as a single unit
```

## Comments — [details](language.md)

```parser
# line comment to end of line
```

## Characters — [details](character.md)

```parser
A = char;        # any single utf-8 character
B = <A:Z>;       # regex block; ranges use ':'
C = \x41;        # hex literal (A)
D = \u0041;  # unicode literal (A)
E = \x43,41,54;  # chain -> "CAT"
F = \x41:5A;     # range A..Z
```

## Counters — [details](counter.md)

```parser
<A:Z>+;      # one or more
<A:Z>*;      # zero or more
<A:Z>?;      # zero or one (optional)
<A:Z>-5;     # exactly 5
<A:Z>-7:12;  # between 7 and 12
```

## Built-in Actions — [details](builtin_action.md)

```parser
spc;   # space
nl;    # newline
eol;   # end-of-line
```

## Inbetween (skip) — [details](inbetween.md)

```parser
stmt = "(" . "A" . ")";  # '.' skips per the config below
. { spc, nl }            # required whenever '.' is used
```

## Variables — [details](variable.md)

```parser
parval p;                  # result of a parse (cannot init)
texval t = "Hello World";  # text
numval n = 50;             # 0..max
semval s = "Cat", "Dog";   # set of text values

A = "A" >> p;              # capture parse result into a variable
B = "B" >> parval x;       # local variable, action-scoped
```

## Permutation — [details](permutation.md)

```parser
A = perm["A" "B" "C"];  # match members in any order
```

## Text Functions — [details](text_function.md)

```parser
tex::order("ABC");   # same length, any character order
tex::oneof("ABC");   # one character from the set
tex::icase("ABC");   # case-insensitive exact match
```

## Parser Result Functions — [details](parser_result_function.md)

```parser
name::is("Fred");      # result equals text
name::not("Amber");    # result does not equal text
name::subkind("Fr");   # result contains substring
name::to_text();       # parsed text
name::to_number();     # parsed text as number
name::length();        # length of parsed text
name::part(1);         # section: 1-indexed char
name::part(1:4);       # section: chars 1..4
name::part(2+);        # section: char 2..end
<A:Z>+::count;         # counter iteration count
name::part(1)::is(\x20); # chain functions
```

## Logic Block — [details](logic_block.md)

```parser
A = {5 * 5 == 25};                          # succeeds when logic is true
B = char >> numval x {x * 2 == 130};        # guard a parse with logic
```

## IF Statement — [details](if_statement.md)

```parser
B = C if({x == 1}) [T|F] D;  # logic true -> T, else F
E = G if(M) [T | F];         # M parses -> T, else F
H = I if(M) [T];             # M parses -> T
J = K if(M) [|F];            # M fails  -> F
```

## Custom Action — [details](custom_action.md)

```parser
indent = _;   # grammar defined externally in user code
custom_action {
    indent: "apm_py_indent",
}
```

## Parser Block — [details](parser.md)

```parser
parser {
    A;        # one lane
    B C;      # a lane with a series
}
```

## AST Customization — [details](abstract_syntax_tree.md)

```parser
(A B)   -> (A B);    # A and B are siblings
(A B)   -> (A (B));  # A is parent of B
(A B C) -> (A B);    # C discarded
```

## Binding Power — [details](binding_power.md)

```parser
bindpow {
    "*" : (8, 9),   # left-associative  (LBP < RBP)
    "^" : (11, 10), # right-associative (LBP > RBP)
}
```

## Config Settings — [details](config_settings.md)

```parser
```
config { <feature> : <value> }
```
