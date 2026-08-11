# Abstract Syntax Tree

The Abstract Syntax Tree (AST) is generated automatically. However, it can be customized. AST customization is only possible with syntac actions. To customize the AST, wrap the grammar on the left in `()`, then use `->` to map it to the `AST` block, which is also contained in `()`.

## AST Rule

AST block:

```parser
A B # A and B are siblings
A (B) # A is parent of B
```

Grammar-AST syntax:
```parser
(A B) -> (A B) # A and B are sibling
(A+ B+) -> (A B) # A... and B... are sibling; U... means U and each additional U added as sibling to the previous U
(A* B*) -> (A B) # A... and B... are sibling; U... means U and each additional U added as sibling to the previous U if exists
(A B) -> (A (B)) # A is parent of B
(A+ B) -> (A (B)) # A... is parent of B; B would be given to the last A
(A B+) -> (A (B)) # A is parent of B...; All Bs would be given to the A
(A (B) C) -> (A B) # A and B are sibling and C is discarded
(A A B) -> (A B) # A and B are sibling; The first A would be chosen and the second A is discarded; You can label to specify.
(`1`A `dog`A B) -> (`dog` B `1`) # second A, B and first A are siblings in that order. Label helps to identify which unit you are referring to.
# labels only apply to the current grammar-ast customization
```

```parser
name = <A:Z>+;
number = <0:9>+;
stmt := (name number) -> (number name);

parser {
    (spc|nl) -> (); # no AST generated; essentially discarded
    stmt;
}
```