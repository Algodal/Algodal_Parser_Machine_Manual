# Config Settings

A grammar can ask the machine to build a different tree. One optional block, at
the top level, with a setting per line:

```parser
config {
    "ast-node-text" : FALSE,
    "ast-node-char" : TRUE,
}
```

Every setting has a default, and what you do not write keeps it. Values are
`TRUE` or `FALSE`; an unknown key is an error, not a shrug.

## What can be set

| setting | default | what it does |
|---|---|---|
| `ast-node-action` | `TRUE` | an action becomes a node |
| `ast-node-text` | `TRUE` | a matched **text literal** becomes a node |
| `ast-node-text-counter` | `TRUE` | `<literal><counter>` makes **one** node, not one per repetition |
| `ast-node-text-series` | `TRUE` | adjacent text literals make **one** node |
| `ast-node-char` | `FALSE` | a matched **character literal** becomes a node |
| `ast-node-char-counter` | `FALSE` | `<char-literal><counter>` makes one node |
| `ast-node-char-series` | `FALSE` | adjacent character literals make one node |

A `-counter` or `-series` setting does nothing while the thing it counts is off,
and turning one on while the other is off is refused rather than ignored.

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
