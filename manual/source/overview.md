# Overview
Version 0.1.0
Released July 7, 2026

---

Algodal Text Parser Generator is a commercial parser generator that generates *LR parsers*. Parser structure includes a Virtual Machine (VM) which is a common code based merged in your projects and the Parser Program which is **"binary"** file representing the parser. The VM runs the parser. This structure allows for one codebase to run many different parsers and increases portability and reduces dependencies.

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
