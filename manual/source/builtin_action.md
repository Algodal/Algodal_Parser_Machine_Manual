# Built-in Action

Some actions are so common that APM builds them in for quick and easy use.

| Action | Grammar |
| :--- | ---: |
| `spc` | parses space: `< \t>` |
| `nl` | parses newline: `"\r\n"|"\r"` |
| `eol` | parses end-of-line: `nl|<end>` |