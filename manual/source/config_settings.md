# Config Settings

```
config {
    .error {
        .format: "%PARSER %MESSAGE custom error",
        .sequencer_message: "unknown character",
        .syntactic_message: "unknown syntax"
    },
    .charseq_buffer_size: 1024,
    .parser_type: .STREAMED, #.BUFFERED 
}

```