# Limits

Fixed ceilings. Most of them are large enough that a grammar meets none of them;
the small ones are small on purpose, and say so.

## The grammar

| | limit |
|---|---|
| actions in one program | 65,535 |
| semvar sets | 4 |
| scopes | 4 |
| positions in one scope | 4 |
| arms in one binding-power table | 64 |
| items in one character class | 65,535 |
| programs linked into one run | 64 |

Four semvar sets is a deliberate ceiling, not an oversight: a set is a global
thing a whole grammar shares, and a grammar that wants a fifth usually wants a
[scope](variable.md) instead.

Four scopes for the same reason, and it follows from the sets. A scope is a
depth counter, and what a depth counter is *for* is emptying the sets bound to
it — a scope with nothing bound to it is refused. So a fifth scope could only
ever govern a set one of the first four already governs. Declaring one is an
error, not a silent truncation.

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
