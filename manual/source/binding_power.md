# Binding Power

Binding power sets the parsing precedence and associativity of operators, which is what you need when parsing expressions. Each operator is given a **left binding power (LBP)** and a **right binding power (RBP)**:

- Right-associative when `LBP > RBP`
- Left-associative when `LBP < RBP`

Binding power is optional, but it is important whenever you parse expressions. The example below builds a small expression parser and then assigns binding powers in a `bindpow` block.

```parser
# Character Sequence is defined with `=`
name = <A:Za:z> (<A:Za:z_0:9>)*;
number = <0> | <1:9> <0:9>+;

# Syntactic Analysis is defined with `:=`
expr := 
    (expr . "+" . expr) -> ("+"(expr expr)) |
    (expr . "-" . expr) -> ("-"(expr expr)) |
    (expr . "*" . expr) -> ("*"(expr expr)) |
    (expr . "/" . expr) -> ("/"(expr expr)) |
    ("(" . expr . ")") -> (expr)  | # anything not included in the AST specification is discarded
    number # default AST
;

## You can choose not to specify the AST and a default AST will be generated
## Example of what that will look like is specified below in comments
# expr := 
#    expr . "+" . expr |
#    expr . "-" . expr |
#    expr . "*" . expr |
#    expr . "/" . expr |
#    "(" . expr . ")"  |
#    number
#;

# Since it is a mix parser (lexing and syntactical analysis occurs at the same time) there is no
# luxury of discarding space tokens. Instead you can use `.` to represent generalized skip and define
# what is skipped.

. { # required if `.` is used in any grammar
    spc, nl # everywhere `.` is used in grammar all the actions defined in this list is called until
    # it can not be called anymore.
};

parser {
    (name . "=" . expr eol) -> ("="(name expr)); 
    name eol;
}

# eol is a built-in action for END-OF-LINE

# OPTIONALLY!!! Parsing precedence can be set for actions
# if these are matched in the parsing, the following binding powers are applied.

# Binding Power
# Right-associative (LBP > RBP)
# Left-associative  (LBP < RBP)

bindpow { # this is completely optional (though important if you are parsing expressions)
    "-"  : (0, 12), # duplicates allowed if lbp is 0
    "!"  : (0, 12),
    "++" : (14, 0),
    "--" : (14, 0),
    "^"  : (11, 10),
    "*"  : (8, 9),
    "/"  : (8, 9),
    "+"  : (6, 7),
    "-"  : (6, 7),
    "<"  : (4, 5),
    "<=" : (4, 5),
    ">"  : (4, 5),
    ">=" : (4, 5),
    "==" : (2, 3),
    "!=" : (2, 3),
}
```