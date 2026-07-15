# Analyzer

The analyzer is a higher lever of the lexer. The lexer operates on the text and produces tokens. The analyzer operates on the tokens and produces syntax (abstract syntax tree). The analyzer can see all tokens unless generated.

```parser
analyzer {
    stmt;
    TRUE / FALSE;
}
```

In the above example, *TRUE* and *FALSE* are tokens. Tokens can also be analyzers - it analyzes itself.

## Syntax Features

To generate an abstract syntax tree we use the *syntax* feature of the analyzer.

```parser
analyzer {
    declaration;
    definition;
    index stmt;
}:: syntax {...}
```

*syntax {...}* automatically generates as thorough as possible syntax tree.

```parser
analyzer {
    declaration;
    definition;
    index stmt B C D;
}:: syntax {
    declaration {...}, # show self and all children
    definition { variable, function }, # show self and only specific children
    stmt {...^{ E, F }}, # show self and all children except only specific children
    ^B {...}, # do not show self but show all children
    C # show only self

    # index and D is not included in abstract tree since not defined.
}
```