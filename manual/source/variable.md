# Variables

A variable keeps something a rule already matched so a later part of the grammar
can use it again. It is declared globally with a type keyword, or declared and
assigned inside an action with `=>`.

| Type | Description |
| :--- | ---: |
| texval | A text value |
| numval | A number value 0 to positive max |
| semval | A set for storing and matching text |

A **parse result** is not a type of its own. Assigning a parse to a variable is
what `=>` does, and the variable's declared type says what is kept: `texval`
keeps the text it matched, `numval` the number that text reads as, `semval` adds
it to a set.

```parser
texval t;
numval n;
semval s;

A = "A" => texval x x::not("C"); # local variable; exists only within action A
B = "B" => t;
C = "C" => n; # auto-conversion
D = "D" => s; # unique results added to set
```

The source of a binding may also be another variable, which copies its value and
consumes nothing:

```parser
E = "E" => texval x x => texval y; # y now holds what x holds
```

## Scope

A variable declared inside an action belongs to that action, and to one entry
into it. Calling the action again -- including recursively -- gives the new
activation its own copy, so an outer value is never disturbed by an inner one:

```parser
w = <a:z>;
rec := w => texval x rec? x;   # an even-length palindrome
```

An alternative that assigns and then loses is rolled back, so only the winning
alternative's assignments survive the choice.

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
