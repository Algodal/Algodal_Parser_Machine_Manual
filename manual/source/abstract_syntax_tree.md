# Abstract Syntax Tree

APM builds the AST for you while it parses. Every syntac action becomes a node
with its units beneath it, and that default is what most grammars want.

```parser
A := B . C;   # A, with B and C as its children, in that order
```

When the shape you want is not the shape the grammar had to be written in, an
**AST map** says what to build instead.

## Writing a map

A map is `->` followed by the shape, and the body it maps must be in
parentheses:

```
(<body>) -> (<map>)
```

Inside the map you name the units of the body. Their **order in the map is
their order in the tree**, whatever order the body matched them in:

```parser
stmt := (name . number) -> (number name);   # number first in the tree
```

Anything you leave out is **discarded**:

```parser
paren := ("(" . expr . ")") -> (expr);   # the brackets do not survive
```

## Making one a parent

`A: (B C)` keeps `A` as a node and puts `B` and `C` underneath it instead of
beside it. A parent can itself be a child, so this nests:

```parser
pair := (name . number) -> (name: (number));
deep := (a . b . c) -> (a: (b: (c)));
```

## `[A]` — lift a node's children

Square brackets **ascend**: whatever `A` held takes `A`'s place, and `A` itself
is dropped.

```parser
up := (name . pair) -> (name [pair]);
```

It moves one level, it does not flatten. What `pair`'s children held stays
where it is.

## `node("Name")` — a node nothing matched

Every other entry in a map points at something the body already produced. This
one is made *because the map asks for it*:

```parser
made := (name => texval v) -> (name node("Extra", v));
```

The second argument is a variable whose captured text becomes the node's value.
Without it you get a node with a name and no value.

## `(C | D)` — either one, in the same place

When two alternatives are wanted in the same slot, name the choice rather than
one side of it:

```parser
item := (label . (number | word)) -> (label: (number | word));
```

## Labels — telling two of the same apart

When a body uses the same action twice, a label says which one you mean. A
label is written in single quotes, **directly against** the unit with no space:

```parser
swap := ('a'name . 'b'name) -> ('b' 'a');
```

Labels exist only for the map they appear in. They never reach the parser.

:::{important}
A map may place each unit **once**. Naming the same thing in two places is
refused (`E-astmap-twice`) — a node has one parent, and a map that asked for
two would have to copy it.
:::

## Renaming with `node_id`

A node is named after the action that made it. To save it under a different
name — one the language reserves, or one that is not an identifier at all — use
a `node_id` block:

```parser
node_id {
    perm_unit: "perm",
    Label: "saved name",
}
```

The grammar goes on referring to the action by its label; only the name
recorded in the tree changes. Each action may be renamed once, and no two
actions may end up saved under the same name.

:::{seealso}
Whether literals become nodes at all, and whether adjacent ones merge, is
settled by [Config Settings](config_settings.md) — worth reading before you
reach for a map, because several shapes are a config change rather than a
rewrite.
:::
