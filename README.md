# Algodal Parser Machine

**Algodal Parser Machine (APM)** is a commercial parser generator that produces
*LR parsers* in C. Instead of emitting one self-contained parser, APM splits a
parser into two parts:

- a **Virtual Machine (VM)** — a shared codebase you integrate into your project
  once, and
- a **Parser Program** — a compact bytecode file unique to each parser.

The VM runs the Parser Program. Because the VM is the same across every parser,
you integrate it once and can then load many different parsers — even several at
the same time. This keeps parsers portable, thread-safe, low on dependencies, and
simple to maintain.

This repository is the official manual for APM and its language, the **Algodal
Parser Machine Language (APML)**.

## Features

- Generates fast, portable LR parsers in C99
- Drops into any C or C++ project, and binds to languages that can call C
  (Python, Java, and more)
- Handles context-heavy and whitespace-sensitive languages (built-in
  indent/dedent handling)
- Semantic predicates and other advanced grammar features
- Reads UTF-8 text and builds the AST for you — no extra code needed
- Simple, keyword-based syntax
- Multiple parsers can run in the same program, across threads
- Compiles for both Windows and Linux
- Syntax highlighting available for VSCode

## Availability

APM is a work in progress. The language design is complete and the tool is
expected to be available by **October 31, 2026**. It can be pre-purchased now, and
buyers get access to the download as soon as it ships.

- Get APM (and the original APG for free):
  https://algodal.itch.io/algodal-parser-generator-tool

## Background: from APG to APM

APM is a complete re-write and re-design of the original **Algodal Parser
Generator (APG)**. APG was simple and fast to write parsers with, but it tokenized
text in a separate pass — which made context-heavy and whitespace-sensitive
languages hard to handle — and it lacked advanced grammar features. APM is the
answer to those limitations. The original APG remains available for free on itch.

## The manual

Read the manual online at:

https://algodal.github.io/Algodal_Parser_Machine_Manual/

The manual is built with [Sphinx](https://www.sphinx-doc.org/) from the Markdown
sources in `manual/source/`.

### Building the manual locally

From the `manual/` directory:

```sh
pip install sphinx myst-parser sphinx-design sphinxcontrib-mermaid sphinx-rtd-theme
make html          # Linux/macOS
make.bat html      # Windows
```

The generated site is written to `manual/build/html/`. Open
`manual/build/html/index.html` in a browser.

Every push to `main` automatically rebuilds and publishes the manual to GitHub
Pages via the workflow in `.github/workflows/deploy-manual.yml`.

## AI Policy

This project follows the AI policy described here:
https://gist.github.com/Rickodesea/1737b9e56152a15e2c5eed7383dbc5ff
