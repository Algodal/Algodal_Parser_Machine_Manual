# Module

Every parser definition is a **module**. A module is the top-level container
for a parser — its actions, its `parser` block and any configuration all live
inside one module.

## Naming a Module

A module is named with the `program` keyword. The declaration usually sits at
the very top of the source.

```parser
program MyParser;
```

A module may also carry a **display name**, written before the identifier:

```parser
program "Nice Name" mp;
```

## Linking Modules

One module can call the actions of another with the `link` keyword. A linked
module is a **separate machine**: it has its own stack, its own globals, its own
semvar sets and its own scopes. Linking does not merge two grammars, it lets one
call into the other.

```parser
program p1;

link p2;

parser {
    "A" . p2::value . "B";
}
```

A linked action is always reached as `module::action`. The qualified name is
required, not decoration — it is what tells a call in `p1` apart from a local
action of the same name.

Link more than one module by repeating the keyword:

```parser
program p1;

link p2;
link p3;

parser { p2::start . p3::start; }
```

The `link "algodal" json;` form is sugar for `link algodaljson;`, exactly as
the two-part `program` declaration is.

## Resolved when it loads, not when it compiles

The other module is **not present** when this one is compiled, so nothing about
it can be checked here — not whether the action exists, and not what kind of
action it is. Those names are carried in the binary and resolved by the loader,
once, when the modules are brought together.

That is the trade for being able to compile modules separately and combine them
later.

:::{seealso}
The `parser` block that drives a module is described in [Parser](parser.md).
A module's own name and every linked handle share the name space actions live
in, so neither may be a [reserved word](keywords.md).
:::
