# Lexer

The parser generator provides a *lexer* structure. Unlike other parser generators, this is not a sieve to simply make tokens from token streams, but it is ordered token generation - a technique that is very similar to *hand written parsers*.

The *lexer* is able to do this by allowing *actions* to be specified as tokenizers. That way, even some tokens match the same text we can parse them separately and unambiguously without any issues.

```parser
lexer {
    "A";
    "B";
    "C";
}
```

The above is very simple, the lexer will first attempt to parse *"A"*, then *"B"* and finally *"C"*. 


```parser
lexer {
    "A" "B" "C";
    "A" "C" "B";
    "C" "B" "A";
}
```

The power of the lexer comes out when we specify more detailed actions. In the first *grammar*. Look at the 1st and the 3rd grammar, they both have "B" as their 2nd unit. If this was a normal sieve, it would failed at this point because it wouldn't be able to differentiate from the 2. But because the lexer knows one grammar starts with "A" and the other starts with "C", it knows specifically that they are *different* "B"'s.

We can use non-literal actions.

```parser
lexer {
    identifier;
    number;
    identifier number value;
    "[" space number space "]";
}
```

The *lexcons* parsed by the lexer doesn't automatically become tokens. You have to choose what becomes a tokens.


```parser
lexer {
    identifier;
    number;
    identifier number value;
    "[" space number space "]";
}::tokens {...}
```

*tokens {...}* tells the lexer to create all possible tokens from the actions.

```parser
lexer {
    identifier;
    number;
    identifier number value;
    "[" space number space "]";
}::tokens {
    identifier,
    value
}
```

In the above case, only identifier and value will become tokens. Everything else is ignored.

## Token Features

```parser
lexer {
    identifier;
    number;
    identifier number value;
    "[" space number space "]";
}::tokens {
    identifier {reduce},
    number {discard},
    value {~discard}
}
```


| Feature | Description |
| :--- | ---: |
| discard | Prevent the token from being seen by the analyzer |
| ~discard | Prevent the token from being seen by the syntax only |
| reduce | If there are multiple occurances of the token in sequence, only select the first |


We can simplify our lexer action using the *inbetween* function.

```parser
lexer {
    identifier;
    number;
    identifier number value;
    ("[" number "]")::inbetween(space);
}::tokens {
    identifier {reduce},
    number {discard},
    value {~discard}
}
```
The *inbetween* inserts space in between the units of the *series*.
