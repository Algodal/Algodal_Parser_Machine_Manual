# Defaults

What the machine does when nothing says otherwise. Everything here can be
changed; nothing here has to be.

## The grammar's own settings

Written in a `config` block — see [Config Settings](config_settings.md).

| setting | default |
|---|---|
| `ast-node-action` | `TRUE` |
| `ast-node-text` | `TRUE` |
| `ast-node-text-counter` | `TRUE` |
| `ast-node-text-series` | `TRUE` |
| `ast-node-char` | `FALSE` |
| `ast-node-char-counter` | `FALSE` |
| `ast-node-char-series` | `FALSE` |
| `scope-ordered-buffer-size` | 64 bytes |
| `cache-call-buffer-size` | 256 slots |

A grammar that writes a size of `0` has written nothing: zero is how "use the
default" is stored, so it cannot also mean "none".

## The run's own settings

Set by whoever starts the run (`ApmVmConfig`), not by the grammar. The runner
`apmr` leaves all of them alone.

| setting | default | what it is |
|---|---|---|
| variable stack | 64 KiB | room for globals and every live action's locals |
| stack growth | off | a grammar that wants more errors instead of growing |
| semvar rows | 64 | rows a set starts with before it doubles |
| call cache | the grammar's | the run may override what the grammar asked for |
| call cache | on | `no_cache` turns it off, which is what tracing wants |
| trace | off | no trace is written unless a writer is given |

The stack does not grow by default on purpose: a parser that wants an unbounded
amount of variable space has nearly always run away, and saying so is worth more
than allocating for it.

## What a rule does when nothing says otherwise

| | default |
|---|---|
| `\|` and `/` | `\|` takes the **longest** match, `/` takes the **first** |
| a counter | greedy, and gives nothing back |
| `.` | skips a run of the inbetween grammar, and only where it is written |
| an action | becomes a node named after itself |
| a semvar | matches its **longest** member; `::first` takes the earliest added |
| a scope | one bracket, and no pairing by position |
