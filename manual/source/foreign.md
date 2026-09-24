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

The actual binding happens at load time, and there are two ways to arrange it.

**Linked in.** Your program hands the machine a table of names and function
pointers, and everything is one binary:

```c
static const ApmForeignAction actions[] = {
    { "apm_py_indent",  MyIndent  },
    { "apm_py_dedent",  MyDedent  },
    { "apm_py_newline", MyNewline },
};

ApmVmForeignConfig fc = { actions, 3, MyInit, MyQuit, NULL };
cfg.foreign = &fc;
```

`init` and `quit` are optional and exist because a matcher that needs state --
an indent stack -- has to be given somewhere to keep it. Whatever `init`
returns becomes the `user` pointer every call receives.

**Loaded.** Build the same file as a shared library and let the stock runner
find the symbols itself:

```
apmr python.apmb file.py --plugin=python_foreign.dll
```

There is no plugin interface to implement: the `foreign` block already names a
**symbol**, so the runner reads those names out of the parser and looks each
one up. Two optional symbols, `apm_plugin_init` and `apm_plugin_quit`, do the
job of `init` and `quit`. One library may own that state; a second that exports
`apm_plugin_init` is refused rather than silently ignored.

The same `.c` file serves both ways, which is what
`assets/samples/python_foreign.c` does.

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
