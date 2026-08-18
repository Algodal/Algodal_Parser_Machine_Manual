# Alias

An alias gives a **label** to a **value**. Wherever the label is referred to, the actual value is used in its place. The following can be aliased: a **character-literal** and its derivatives, a **character-block**, a **number**, and **text**.

```parser
program example;

alias letter <A:Z>; # character-block
alias code \x41; # character-literal
alias bigcode \x41:43; # range
alias chaincode \x41,42,43,44; # chain
alias x 100; # number
alias animal "CAT"; # text

A = letter;
```