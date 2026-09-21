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

A map never changes what was **matched**. It only decides what is kept and
where it hangs.

## Making one a parent

`A: (B C)` keeps `A` as a node and puts `B` and `C` underneath it instead of
beside it. A parent can itself be a child, so this nests:

```parser
pair := (name . number) -> (name: (number));
deep := (a . b . c) -> (a: (b: (c)));
```

## A name means every unit of that name

This is the rule the whole map works by, and it is worth saying plainly: a name
in a map means **every unit of that name in the body**, and they all go to the
same place.

```parser
X := (A . A . B) -> (B: (A));
```

Over `a a b`, both `A`s land under `B`. A counter is the same idea — one
instruction making many nodes, all going to the one slot.

Used as a **parent**, the name still means all of them, so the most recent one
is the one that takes the children:

```parser
X := (A . A . B) -> (A: (B));   # the second A is B's parent
```

That is not a mistake to be reported. If you meant one of them in particular,
label it.

## Reaching into a choice

A map can name something that only *one* alternative produces:

```parser
X := (A . (B | C) . D) -> (A: (C));   # C when C matched; nothing when B did
```

Or it can name the **choice itself**, when either side is wanted in the same
place. This is the form to reach for when a symbol appears in every
alternative:

```parser
X := (A . (B | C) . D) -> (A: ((B|C)) D);   # whichever one matched
```

Writing `(B|C)` says "the thing this choice produced", so the map does not have
to be written twice.

## `[A]` — lift a node's children

Square brackets **ascend**: whatever `A` held takes `A`'s place, and `A` itself
is dropped. It moves one level; what those children held stays put.

Given `P := A . B;` the difference is:

```parser
X := (P . C) -> (C: (P));     # (X (C (P (A) (B))))    P stays
X := (P . C) -> (C: ([P]));   # (X (C (A) (B)))        P goes, A and B arrive
X := (P . C) -> ([P] C);      # (X (A) (B) (C))        at the top
X := (P . C) -> (C [P]);      # (X (C) (A) (B))        keeping its place
```

An ascended node keeps the **position** it had among its siblings; only the
level goes. This is how you flatten one wrapper that the grammar needed but the
tree does not.

`[A]` cannot be a parent — there would be no `A` left to hang anything on.

## `node("Name")` — a node nothing matched

Every other entry in a map points at something the body already produced. This
one is made **because the map asks for it**.

```parser
made := (name => texvar v) -> (name node("Extra", v));
```

Once made it is a node like any other: it can be a parent, it can be a child,
and it nests.

```parser
wrap := (a . b) -> (node("Group"): (a b));   # a made node as the parent
```

The second argument names a variable, and the text that variable holds becomes
the node's value — a span of the input, like every other node's value. Nothing
anywhere invents text. Without it you get a node with a name and no value.

Because the node is emitted at the end of the body, a variable it reads has
already been written by the time it runs.

## Everything is reachable

A map names a maker the way it is **written**. An action by its name, a literal
by itself, a character block by the block text, a linked call by the whole
qualified name:

```parser
X := (<a:z> . B) -> (B: (<a:z>));
Y := (javascript::stmt . B) -> (B: (javascript::stmt));
```

There is no kind of maker a map cannot point at.

:::{note}
A character block only *makes* a node when `ast-node-char` is on — see
[Config Settings](config_settings.md). A map can name it either way, but with
that setting off there is no node to place.
:::

## Labels — telling two of the same apart

A plain name already means all of them, so you only need a label when two units
of one name must go to **different** places. A label is written in single
quotes, directly against the unit with no space:

```parser
swap := ('a'name . 'b'name) -> ('b' 'a');
```

A labelled unit answers **only** to its label, which is what leaves the plain
name free for the other one. Labels exist only for the map they appear in and
never reach the parser.

:::{important}
A map may place each thing **once**. Naming the same unit in two places is
refused — a node has one parent, and a map that asked for two would have to
copy it.
:::

## Renaming with `node_id`

A node is named after the action that made it. `node_id` changes the name it is
**saved** under, while the grammar goes on calling the action by its label.

```parser
node_id {
    perm_unit: "perm",
    ident_node: "identifier",
}
```

The reason this exists: **when the name you want is a keyword.** Every word the
language spells out is [reserved](keywords.md), so no action can be called
`perm`, `char` or `end`. Label the action something else and use `node_id` to
save it under the name you actually wanted.

APM's own grammar does exactly that — its rule for a permutation is labelled
`perm_unit` and saved as `perm`.

The saved name must be a **usable identifier** — letters, digits and
underscore, not starting with a digit. Whatever reads the tree will have to
write that name in its own source, so a name with a space or a dash in it is
refused.

Each action may be renamed once, and no two actions may end up saved under the
same name.

:::{seealso}
Whether literals become nodes at all, and whether adjacent ones merge, is
settled by [Config Settings](config_settings.md) — worth reading before you
reach for a map, because several shapes are a config change rather than a
rewrite.
:::
