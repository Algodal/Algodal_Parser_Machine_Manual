# Parser

The parser lexes the incoming text to generate character sequences and then analyzes generated character sequences into syntactic blocks simultationly. That is, it builds the AST the same time as it is generating tokens. It is a top-down parser that provides **lanes** of series. Each lane is **parsed** simultaneously until a single lane is selected. Lanes are not exactly the same options as there are minor differences that make lanes drive the parsing.

```
parser {
    # expects syntac or charseq actions
}
```

```
parser {
    A; # single lane
}
```

```
parser {
    A;
    B;
    C; # 3 lanes
}
```

```
parser {
    A B C; # this lane has a series of multiple units
    # this gives it more context
}
```

```
parser {
    A B C D; # lane 1 and 2 are similar but differ at the 4th unit
    A B C F;
}
```
