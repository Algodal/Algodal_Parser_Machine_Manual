# Overview
Version 0.1.0
Released July 7, 2026

---

Algodal Parser Machine (APM) is a commercial parser generator that generates *LR parsers*. A parser is made of two parts: a **Virtual Machine (VM)**, a shared codebase you merge into your project, and a **Parser Program**, a *"binary"* file that represents one specific parser. The VM runs the Parser Program.

This structure lets a single codebase run many different parsers, which increases portability and reduces dependencies.

:::{note}
Because the VM is the same across every parser, you only integrate it once. Swapping to a different grammar is just a matter of loading a different Parser Program.
:::

```{mermaid}
flowchart TD
    Text["Text Being Parsed<br/>(Buffer / File)"]
    Parser["Parser Program<br/>(unique to each parser)"]
    VM["Virtual Machine<br/>(same across parsers)"]
    Tokens["Tokens"]
    AST["Abstract Syntax Tree"]

    Text --> VM
    Parser --> VM
    VM --> Tokens
    VM --> AST
```
