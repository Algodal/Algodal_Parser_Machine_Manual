# Limits

Fixed ceilings. Most of them are large enough that a grammar meets none of them;
the small ones are small on purpose, and say so.

## The grammar

| | limit |
|---|---|
| actions in one program | 65,535 |
| semvar sets | 16 |
| scopes | 16 |
| positions in one scope | 7 |
| arms in one binding-power table | 64 |
| items in one character class | 65,535 |
| programs linked into one run | 64 |

Sixteen semvar sets is a ceiling, not an oversight: a set is a global thing a
whole grammar shares, and a grammar that wants a seventeenth usually wants a
[scope](variable.md) instead.

Sixteen scopes, the same as the sets: more kinds of bracket than any language
nests. Declaring a seventeenth is an error, not a silent truncation.

Seven positions in one scope because that is what its three count bits hold —
every count the field can store is a legal scope, and none is wasted.

## The run

| | limit |
|---|---|
| variable stack | 64 KiB, or 64 MiB if it is allowed to grow |
| binding-power nesting | 128 levels |
| nesting of one ordered scope | its buffer, 64 bytes by default |

## Plugins

| | limit |
|---|---|
| shared libraries per run | 8 |
| foreign symbols bound | 64 |
| length of a foreign name | 96 bytes |

## What is not limited

The input, the AST, a semvar set, and how deep a rule may call itself are all
bounded by memory rather than by a constant. An action that recurses without
consuming will exhaust the variable stack and be told so.
