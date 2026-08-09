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

A = "A" >> parval x x::not("C"); # local variable; exits only on action A
B = "B" >> p;
C = "C" >> t; # auto-conversion
D = "D" >> n; # auto conversion
E = "E" >> s; # unique results added to set
```
