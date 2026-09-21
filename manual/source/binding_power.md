# Binding Power

Write an expression grammar the way you would say it, and the parse comes out
wrong: `2 * 3 + 5` groups by how the recursion happened to fall rather than by
what arithmetic means. **Binding power** is how you tell APM what the operators
are worth.

A rule bound to a table is parsed by a precedence loop instead of a greedy
tail. Left recursion in the rule is fine — write it directly.

## The table

Each operator gets two numbers: a **left binding power** and a **right binding
power**. Entries end with `;`.

```parser
bindpow bp {
    "or"  : (10, 11) ;
    "and" : (20, 21) ;
    "=="  : (30, 31) ;
    "<"   : (40, 41) ;
    "+"   : (50, 51) ;
    "-"   : (50, 51) ;
    "*"   : (60, 61) ;
    "/"   : (60, 61) ;
    "not" : (0, 70) ;
}
```

Higher numbers bind tighter, so `*` takes its operands before `+` gets a look.

## Associativity is the gap, not a keyword

There is no `left` or `right` to write. The relationship between the two
numbers **is** the associativity:

| | |
| :--- | :--- |
| `r = l + 1` | left-associative — `a - b - c` is `(a - b) - c` |
| `r = l - 1` | right-associative — `a ^ b ^ c` is `a ^ (b ^ c)` |

## Prefix and postfix are a zero

A side that binds nothing is `0`, and that is also how the kind is written:

| | |
| :--- | :--- |
| `(0, r)` | prefix — `not a` |
| `(l, 0)` | postfix — `a++` |
| `(l, r)` | infix — `a + b` |

The slot is genuinely dead, so a `0` can never be mistaken for a real power. A
prefix arm is only ever matched where an operand is expected, where nothing
reads its left; a postfix arm folds immediately, so nothing reads its right.

What decides which kind an occurrence *is* is the **grammar** — where the
alternative sits — not what the table calls it. The table only supplies the
numbers.

## Binding a rule to a table

`feat {"bind": <table>}` in front of the definition:

```parser
feat {"bind": bp} expr := atom
      | expr . "or"  . expr
      | expr . "and" . expr
      | expr . "=="  . expr
      | expr . "<"   . expr
      | expr . "+"   . expr
      | expr . "-"   . expr
      | expr . "*"   . expr
      | expr . "/"   . expr
      | "not" . expr
      ;

atom  := number | string | ident | group;
group := "(" . expr . ")";
```

The first alternative that is not an operator arm is the **operand** — here
`atom`. The rest are the arms, and each must name an operator the table
declares.

:::{important}
Every operator the rule writes must appear in the table, and every operator in
the table must appear in the rule. An operator that is not declared simply ends
the expression, which would silently truncate a parse rather than fail it —
so it is refused when the grammar is validated.
:::

:::{seealso}
`bindpow` and `feat` are [reserved words](keywords.md), and a table's name
shares the name space actions live in.
:::
