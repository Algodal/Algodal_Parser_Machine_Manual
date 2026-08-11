# Parser

The parser lexes the incoming text into character sequences and analyzes those sequences into syntactic blocks *simultaneously*. That is, it builds the AST at the same time as it generates tokens. It is a top-down parser that provides **lanes** of series. Each lane is **parsed** simultaneously until a single lane is selected. Lanes are not quite the same as options — there are minor differences that let lanes drive the parsing. Lanes are syntactic actions, that is, they generate AST.

```parser
parser {
    # expects syntac or charseq actions
}
```

```parser
parser {
    A; # single lane
}
```

```parser
parser {
    A;
    B;
    C; # 3 lanes
}
```

```parser
parser {
    A B C; # this lane has a series of multiple units,
    # which gives it more context
}
```

```parser
parser {
    A B C D; # lanes 1 and 2 are similar but differ at the 4th unit
    A B C F;
}
```
