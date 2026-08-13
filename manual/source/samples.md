# Samples

**BASIC**

```parser
# BASIC LANG
# ---------
# A 100
# B  25

program Basic; # every parser is a module named with `program`

parser {
    # action      ->  ast: (node(children)...)
    (name number) -> (name(number)); # generate name with number as child of name
    (spc | nl) -> (); # no AST generated
}

name = <A:Z>+; # character sequence
number = <0> | <1:9> <0:9>+; # character sequence

# spc is built-in rule for space
# nl is built-in rule for newline
```

**ADVANCE**

```parser
# ADVANCE LANG
# X = 23 + 5 * (6 - 4)
# X

program Advance;

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

# OPTIONALLY!!! Parsing Precidence can be set for actions
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

**CHALLENGE**

```parser
# CHALLENGE LANG
# X:
#   Y
#   Z
# A     X

# In special cases the parser generator via standard library or user may provide
# functions that allows for complex parsing that the syntaxical grammar can not 
# support.

# The parser generator standard library provide functions for python indentation.
# If the user wants haskel indentation, they can write their own functions.
# Functions are expected to be written externally in C (or any language binding 
# to C ABI and as long as the user can run the parser in that language's ecosystem).

name = <A:Za:z> (<A:Za:z_0:9>)*;
structure1 := name . ":" . indent (name newline)* dedent;
structure2 := name special_tab name;

# placeholder definition of actions (REQUIRED!)
indent = _; # indicates that the action grammar is defined externally through user customized code.
dedent = _;
special_tab = _;
newline = _;

# Reference linking of the custom action with user code. Actual linking is done outside DSL.
# User code is called on text where ever action is used to generate syntactic objects.
custom_action { 
    indent: "apm_py_indent",
    dedent: "apm_py_dedent",
    newline: "apm_py_newline",
    special_tab: "myfunc"
}
```

**FEATURES**

```parser
# 1. Variables

# Parser Type
# Captures the result of a parse.
# Automatically cast to a text or number based on use. Can do explicit cast as well.
# Can not initialize

parval x;




# Text Type
# Holds a literal text (aka string).
# Can be initialized

texval y;
texval z = "Hello World";

# Number Value
# Holds 0 or a Positive number. (Negative Numbers are not supported).
# Can be initialized.

numval a;
numval b = 50;
numval c =  0; # range

# Semantic Type
# A set of parser type. Each type you assign a value to it, if the value is different to all the values
# in the set then the value is added to the set.
# It can be used in parsing, it does a exact match of the text against all its values in the set.
# Can not be used like a regular Text or Number type.
# Can be initialized with a list of text only;

semval d;
semval e = "Cat";
semval f = # all values are added to the set
    "Cat",
    "Dog",
    "Rat",
    "Bat";

#2. Assignment of Variables

parval x;  # global variable

A = "bone" >> x; # >> grammar assigns the result of a parse to its variable
B = "bone" >> parval y; # local variable definition is supported. Variable exists only in the action.

#3. Conversion

parval a;

A = "2" >> a;
B = a; # a is auto-converted to text and parsed for an exact match
C = "x"-a; # a is auto-converted to number applied to counter.
D = tex::icase(a::to_text()) "x"-(a::to_number()); # explicit conversion

# 4. Permutation
# The parser can match a series of actions in any order using permutations.

A = perm["A" "B" "C"] "D";

# 5. Logic Block
# Logic block allows the specification of non-parsing logic which can be mathematical logic
A = {5 * 5 == 20};
B = char >> numval x >> numval y {y = 15; x * y == 65};

# 6. IF statement
# Parsing can branch conditionally

numval x = 0

A = char >> x; # auto-conversion to numval
B = C if({x == 1}) [T|F] D; # if logic is true then parse T else parse F
E = G if(M) [T | F]; # if M parses, then parse T else parse F
H = I if(M) [T];  # if M parses, then parse T
J = K if(M) [|F]; # if M fails to parse then parse F

# 7. Text Functions

A = tex::order("ABC"); # similar to perm for syntactic objects
B = tex::oneof("ABC"); # a single character from the text
C = tex::icase("ABC"); # exact but with any case

# 8. Parser Result Functions

name = <A:Za:z>+;
t1 = name::is("Fred"); # or name >> parval x x::is("Fred"); | checks if the result equals "Fred"
t2 = name::subkind("Fr"); # checks if result has substring called "Fr"
t3a = name::part(1); # section the result; returns first character; 1 index based
t3b = name::part(1:4); # section the result; returns first to fourth character
t3c = name::part(2+); # section the result; returns second to last character
t3d = name::part(1)::is(\x20); # chain functions
t3e = name::part(3:4)::is("ed"); # chain functions
t4a = name::not("Amber"); # checks that the result is not text "Amber"
t4b = char::not("A"); # your checks should be relative to the size
t4c = char::not(tex::oneof("hello")); # can pass text functions as parameters
t4d = char*::not("This"); # no difference with counters

# 9. Config Settings

# Some config settings can be set within the language itself.

config {
    .error {
        .format: "%PARSER %MESSAGE custom error",
        .sequencer_message: "unknown character",
        .syntactic_message: "unknown syntax"
    },
    .charseq_buffer_size: 1024,
    .parser_type: .BUFFERED,
}


```