# Variables

Variables can be defined globally using variable type keyword as well as be defined and/or assigned within an action using `>>`.

| Type | Description |
| :--- | ---: |
| parval | The result of a parse |
| texval | A text value |
| numval | A number value 0 to positive max |
| semval | A set for storing and matching parval to incoming text |

```parser
parval p;
texval t;
numval n;
semval s;

A = "A" >> parval x x::not("C"); # local variable; exists only within action A
B = "B" >> p;
C = "C" >> t; # auto-conversion
D = "D" >> n; # auto conversion
E = "E" >> s; # unique results added to set
```

## Global Initialization

Global variables can also be initialized with a value when they are declared.

```parser
texval greeting = "Hello World"; # text value
numval limit = 50;               # number value
semval animals =                 # set of text values
    "Cat",
    "Dog",
    "Rat";
```

:::{warning}
A `parval` **cannot** be initialized — it only ever holds the result of a parse. Declare it without a value (`parval x;`) and assign to it with `>>` during parsing.
:::
