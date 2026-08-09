# Alias

Alias provides a way to **label** *values*. When the label is referred to, the actual value is used. The following can be aliased: **character-literal** and its derivatives, **character-block**, **number** and **text**.

```
alias letter <A:Z>; # character-block
alias code \x41; # character-literal
alias bigcode \x41:43; # range
alias chaincode \x41,42,43,44; # chain
alias x 100; # number
alias animal "CAT"; # text

A = letter;
```