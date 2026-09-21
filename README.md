# Algodal Parser Machine

**Algodal Parser Machine (APM)** is a parser generator that produces
*LL parsers* in C. Instead of emitting one self-contained parser, APM splits a
parser into two parts:

- a **Virtual Machine (VM)** — a shared codebase you integrate into your project
  once, and
- a **Parser Program** — a compact bytecode unique to each parser.

The VM runs the Parser Program. Because the VM is the same across every parser,
you integrate it once and can then load many different parsers — even several at
the same time. This keeps parsers portable, thread-safe, low on dependencies, and
simple to maintain.

This repository is the official manual for APM and its language, the **Algodal
Parser Machine Language (APML)**.

## Features

- Generates fast, portable LL parsers in C99
- Drops into any C or C++ project, and binds to any language that supports C ABI
- **Scannerless** — lexing and parsing share one context, so context-heavy and
  whitespace-sensitive languages are no longer a wall
- Reads UTF-8 text and builds the AST for you — no extra code needed
- **AST maps** reshape the tree, so the grammar is written for clarity rather
  than for the shape you happen to need
- **Pratt parsing** with binding powers, and left recursion written directly
- Semantic predicates via `semvar` sets, with `scope` for block scoping
- Text and number variables, logic blocks and `if`, for grammars that decide
- **Custom actions** let a rule body live in your C code, for things no grammar
  can state — Python indentation, for one
- **Linking** calls into another parser program, resolved when it loads
- Simple, keyword-based syntax with a short list of reserved words
- Multiple parsers can run in the same program, across threads
- Code is compatible for all platforms you can build C99 code on (minus dependency requirements)
- Syntax highlighting available for VSCode

## Availability

APM is a work in progress. The language design and the tool is ongoing and is
expected to be available in full no later than **October 31, 2026**. It can be pre-purchased now, and
buyers get access to the download as soon as it ships.

- Get APM (and the original APG for free):
  https://algodal.itch.io/algodal-parser-machine

## Background: from APG to APM

APM is a complete re-write and re-design of the original **Algodal Parser
Generator (APG)**. APG was simple and fast to write parsers with, but it tokenized
text in a separate pass — which made context-heavy and whitespace-sensitive
languages hard to handle — and it lacked advanced grammar features. APM is the
answer to those limitations and provides much more. The original APG remains available for free on itch.

## The manual

Read the manual online at:

https://algodal.github.io/Algodal_Parser_Machine_Manual/


### Building the manual locally

From the `manual/` directory:

```sh
pip install sphinx myst-parser sphinx-design sphinxcontrib-mermaid sphinx-rtd-theme
./make html          # for web version
```

The generated site is written to `manual/build/html/`. Open
`manual/build/html/index.html` in a browser.


## AI Policy

This project follows the AI policy described here:
[Open Professional AI Policy](https://gist.github.com/Rickodesea/1737b9e56152a15e2c5eed7383dbc5ff)
