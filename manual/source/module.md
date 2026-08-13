# Module

Every parser definition is a **module**. A module is the top-level container for a parser — its actions, its `parser` block, and any configuration all live inside one module.

## Naming a Module

A module is named with the `program` keyword. The declaration usually sits at the very top of the source.

```parser
program MyParser;
```

## Linking Modules

One module can reuse the actions of another by referring to it with the `link` keyword. Once linked, the actions of the linked module are available by name, just like locally defined actions.

```parser
program p1;

link p2; # bring the actions of module p2 into scope

parser {
    "A" p2 "B"; # p2 is an action provided by the linked module
}
```

You can link more than one module — repeat the `link` keyword for each.

```parser
program p1;

link p2;
link p3;

parser {
    p2 p3;
}
```

:::{seealso}
The `parser` block that drives the module is described in [Parser](parser.md). Actions referenced across modules follow the same rules as local [Actions](language.md).
:::
