# Overview
Version 0.1.0
Released July 7, 2026

---

Algodal Parser Machine (APM) generates *LL parsers*, but with a twist. Instead of emitting one self-contained parser, it splits a parser into two parts: a **Virtual Machine (VM)**, a shared codebase you merge into your project, and a **Parser Program**, a bytecode file that represents one specific parser. The VM runs the Parser Program.

This structure lets a single codebase run many different parsers, which increases portability, adds thread safety, reduces dependencies and reduces complexity.

:::{note}
Because the VM is the same across every parser, you only need to integrate the VM codebase once. Then you can dynamically load different parsers (even multiple parsers at the same time).
:::

```{mermaid}
flowchart TD
    Text["Text Being Parsed<br/>(Buffer / File)"]
    Parser["Parser Program<br/>(unique to each parser)"]
    VM["Virtual Machine<br/>(same across parsers)"]
    AST["Abstract Syntax Tree"]

    Text --> VM
    Parser --> VM
    VM --> AST
```

## Background: From APG to APM

APM is a complete re-write and re-design of my previous parser generator, **Algodal Parser Generator** (APG).

I built APG because I wanted a parser generator that was simpler and faster to write than the traditional tools. It worked — you could stand up a JSON parser in an afternoon — but it had real limitations that I kept running into:

- **It struggled with context-heavy languages.** APG tokenized text in a separate pass, so languages whose meaning were complex were painful or impossible to handle cleanly.
- **It struggled with whitespace languages.** APG had no streamline way of handling indent and dedent parsing for languages like Python.
- **No advanced grammar features.** There were no semantic predicates or similar escape hatches, so grammars that needed to make decisions based on context had nowhere to go.
- **Command-style syntax.** APG used `@<name>` commands instead of keywords, chosen to avoid reserved words. Reviewers of the language told me they would prefer familiar keywords.

APM is my answer to these: scanning and parsing share the same context so context-heavy languages are no longer a wall, indent/dedent handling is built in for whitespace-sensitive languages, semantic predicates give grammars a real escape hatch, and the syntax moves from `@<name>` commands to simple keywords.

APG is still available for free if you want to see where this started. Both versions are on [itch](https://algodal.itch.io/algodal-parser-generator-tool).

