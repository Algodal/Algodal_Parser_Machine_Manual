# Config Settings

Some settings can be configured from within the language itself using a `config` block. The block is part of the grammar, so it lives alongside your actions in the same source.

```parser
config {
    .error {
        .format: "%PARSER %MESSAGE custom error",
        .sequencer_message: "unknown character",
        .syntactic_message: "unknown syntax"
    },
    .charseq_buffer_size: 1024,
    .parser_type: .BUFFERED,
}
```