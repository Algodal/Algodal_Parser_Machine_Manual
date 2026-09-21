# Foreign Bodies

Some things a grammar cannot say. Python's indentation is the standard example:
what counts as an indent depends on a stack of previous indents, which is not a
shape any amount of EBNF will describe.

For those, an action's body can live **outside the grammar**, in C you write.

## Declaring one

`_` as the body says "this action is defined elsewhere":

```parser
indent  = _;
dedent  = _;
newline = _;
```

The action is declared, named and usable like any other. It simply has no
grammar.

## Binding it to your code

A `foreign` block says which function stands behind each one. The name on
the left is the action; the string on the right is what your program registers
the function under:

```parser
foreign {
    indent:  "apm_py_indent",
    dedent:  "apm_py_dedent",
    newline: "apm_py_newline",
}
```

The actual binding happens in your program, at load time, by registering a
function under that name.

## Using one

A foreign body is a **matcher**, exactly as `char` is. It reads text and says
how many bytes it took; it makes no node of its own. The action around it owns
whatever it matched, the same way it would over a literal:

```parser
name  = <A:Za:z> . (<A:Za:z_0:9>)*;
block := name . ":" . indent . (name . newline)* . dedent;
```

Every call site stays an ordinary call, so nothing else in the grammar needs to
know the body is not grammar.

:::{important}
The placeholder declaration is required. `_` is what tells the compiler the
action is deliberately bodiless rather than forgotten.
:::

:::{seealso}
`foreign` is a [reserved word](keywords.md). The names inside the block
are quoted strings, so they are free of that restriction.
:::
