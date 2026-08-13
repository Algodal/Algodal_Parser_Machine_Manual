# Abstract Syntax Tree

The Abstract Syntax Tree (AST) is generated automatically for all syntac actions. By default, all charseq and syntac in the grammar ends up in the AST. To customize the AST, the **AST grammar** is used.

AST grammar are defined along side Action grammar using `->`. Both the AST and Action grammar is required to be contained in `()`.

## AST Grammar

```
(<Action>) -> (<AST>);
```

**AST PART**:
```
SIBLING_1 SIBLING_2
```
```
PARENT (CHILD_1 CHILD_2)
```

## AST Default Generation
```parser
A := B C; # Generates A as parent of B and C
          # in that order
```

## AST Custom Generation
```parser
A := (B C) -> (B (C)); # Generates A as parent of B
                       # and B as parent of C
```


Grammar-AST syntax:
```parser
(A B) -> (A B) # A and B are sibling
(A+ B+) -> (A B) # A... and B... are sibling; <U>... means U 
                 # and each additional U added as sibling to the previous U
(A* B*) -> (A B) # A... and B... are sibling; <U>... means U and each 
                 # additional U added as sibling to the previous U if exists
(A B) -> (A (B)) # A is parent of B
(A+ B) -> (A (B)) # A... is parent of B; B would be given to the last A
(A B+) -> (A (B)) # A is parent of B...; All Bs would be given to the A
(A (B) C) -> (A B) # A and B are sibling and C is discarded
(A A B) -> (A B) # A and B are sibling; The first A would be chosen 
                 # and the second A is discarded; You can label to specify.
(`1`A `dog`A B) -> (`dog` B `1`) # second A, B and first A are siblings in 
                                 # that order. Label helps to identify 
                                 # which unit you are referring to.
                                 # labels only apply to the 
                                 # current grammar-ast customization
(A+ B+ C) -> (A^ B C) # A^... and B.... and C are sibling; <U>^.... means each
                      # each additional A becomes a child of the previous A
(A+ B+ C) -> (A^1 B C) # A^... and B.... and C are sibling; <U>^1.... means each
                      # each additional A becomes a child of the 1st A
(A+ B+ C) -> (A B C!) # A... and B.... and C! are sibling; <U>! means each
                      # do not save U but save any children of U in its place
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