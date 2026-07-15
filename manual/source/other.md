# Other

Other features of the ATPGL.

## Alias

Instead of using literals everywhere, you can use alias which is *good programming* convention.

```parser
alias alpha "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alias digit <0-9>
alias max   15

A = [+]oneof alpha;
B = digit+;
C = [max]"D";
```

## Variables

The parser generator can create and use variables. `->` is used to assign variables during an action. `->` may have `()` for its parameter on the left. You may also define local variables on the action.

| Type | Description |
| :--- | ---: |
| parval | The result of a parse |
| texval | A string literal |
| numval | Counting number from 0 to maximum |
| tabval | A table for storing parval and then using one of them literal text for parsing |

```parser
parval p
texval t
numval n
tabval b

A = "A" -> parval x x::not("C"); # local variable; exits only on the action
B = "B" -> p;
C = "C"::tex() -> t
D = "D"::len() -> n
E = "E" -> b
```

## Scope

This is an extremely advance and niche feature. It applies to variables. It creates a new copy of the variable when used in a different scope. This is to support advanced languages.

```parser
scope {
    ("{", "}"): {b} 
}
```

In the above example, `"{"` and `"}"` must be tokens. Each time the parser generator sees `"{"` token it creates a new scope and at `"}"` it exits the scope. `b` is the global variable.