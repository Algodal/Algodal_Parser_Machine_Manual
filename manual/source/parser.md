# Parser

The parser lexes the incoming text into character sequences and analyzes those sequences into syntactic blocks *simultaneously*. That is, it builds the AST at the same time as it generates tokens. It is a top-down parser.

The parser block names the **start grammar** — the single grammar the parser begins from. Parsing runs it from the front of the input; when it returns a match and text remains, the parser runs it **again** from where it left off, and so on until the input is consumed or a run matches nothing. Each run is one top-level block. There is exactly one start grammar.

```parser
parser {
    main_grammar;   # the single start grammar (a syntac/charseq action, an option, a series, or any unit)
}
```

The start grammar can be a **labeled action**:

```parser
parser {
    my_action;
}
```

an **option**:

```parser
parser {
    "A" | "B" | "C";
}
```

any single **unit**:

```parser
parser {
    "A";
}
```

or a **series**:

```parser
parser {
    "A" "B" "C" "D";
}
```

## Repetition is the loop; separators are `.`

Because the parser re-runs the start grammar over what remains, a grammar of adjacent items needs no counter — the loop walks them:

```parser
parser {
    item;   # the loop repeats it: item item item ...
}
```

The loop does **not** skip anything between runs. Inbetween is the `.` building block — it runs the configured skip only where `.` appears in the grammar. So when items are separated (e.g. by spaces), put `.` where the separator goes:

```parser
parser {
    item (. item)*;   # items separated by the inbetween
}
. { spc }
```
