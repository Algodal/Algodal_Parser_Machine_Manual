# Config Settings

A grammar can ask the machine to build a different tree. One optional block, at
the top level, with a setting per line:

```parser
config {
    "ast-node-text" : FALSE,
    "ast-node-char" : TRUE,
}
```

Every setting has a default, and what you do not write keeps it. An unknown
key is an error, not a shrug.

A setting is either a **switch**, written `TRUE` or `FALSE`, or a **size**,
written as a number. A value of the wrong kind, or a size outside its range, is
refused when the grammar is compiled.

## What can be set

| setting | kind | default | what it does |
|---|---|---|---|
| `ast-node-action` | switch | `TRUE` | an action becomes a node |
| `ast-node-text` | switch | `TRUE` | a matched **text literal** becomes a node |
| `ast-node-text-counter` | switch | `TRUE` | `<literal><counter>` makes **one** node, not one per repetition |
| `ast-node-text-series` | switch | `TRUE` | adjacent text literals make **one** node |
| `ast-node-char` | switch | `FALSE` | a matched **character literal** becomes a node |
| `ast-node-char-counter` | switch | `FALSE` | `<char-literal><counter>` makes one node |
| `ast-node-char-series` | switch | `FALSE` | adjacent character literals make one node |
| `scope-ordered-buffer-size` | size | `64` | bytes of nesting a [positioned scope](variable.md) gets, one byte per open level. 8 to 4096 |
| `cache-call-buffer-size` | size | `256` | slots in the run's call cache, rounded up to a power of two. 8 to 1048576 |

A `-counter` or `-series` setting does nothing while the thing it counts is off,
and turning one on while the other is off is refused rather than ignored.

## The two sizes

```parser
config {
    "scope-ordered-buffer-size" : 128,
    "cache-call-buffer-size"    : 1024,
}
```

Neither changes what a grammar means. `scope-ordered-buffer-size` is how deep a
scope with [positioned brackets](variable.md) may nest before the parse fails
saying so — one byte per open level, per ordered scope. `cache-call-buffer-size`
is how many results the run remembers so that the same rule at the same place is
not walked twice; more slots means fewer misses and more memory.

Write them when the language asks for it: a deeply nested document needs the
first, a large grammar over a large file the second. The defaults are right for
everything else.

## Literals in the tree

```parser
kv := key ":" value;
```

With `ast-node-text` on — the default — `port:8080` gives three children:

```
kv
  key   "port"
  text  ":"
  value "8080"
```

The `":"` node has no action to be named by, so it is named by **what it
matched**. That is forced rather than chosen: `tex::icase("AND")` matches `and`,
and `tex::oneof("abc")` matches one character out of three, so the literal in the
grammar would be the wrong label in both cases.

Turn it off and the literal matches and consumes exactly as before, silently:

```parser
config { "ast-node-text" : FALSE }
```

## One node, not many

Adjacent literals say one thing, so they make one node:

```parser
z := "A" "B";                    ->  text "AB"
z := tex::oneof("abc")-5;        ->  text "aabcb"
z := "A" "C"-5 "D";              ->  text "ACCCCCD"
```

A **`.`** between two literals ends the run — the grammar separated them, and
whether the input happened to put nothing between them is not the grammar's
business:

```parser
z := "a" . "b";                  ->  text "a",  text "b"
```

So does anything that is not a literal:

```parser
z := "a" w "c";                  ->  text "a",  w,  text "c"
```

## Parsing with no tree at all

Turn everything off and nothing is built. The parse still says what it matched
and how far it got, which is all a recogniser needs:

```parser
config { "ast-node-action" : FALSE, "ast-node-text" : FALSE }
```

With actions off but literals on, the levels go and the literals stay.

:::{warning}
**Changing a setting changes the AST — that is what it is for.** An AST
interpreter is written against one config, so changing one is a breaking change
for whatever reads the tree.
:::

:::{note}
Optimized and unoptimized builds produce **identical** trees, whatever the
config. The optimizer declines any rewrite it cannot make invisible.
:::
