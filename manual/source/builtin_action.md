# Built-in Action

Some action are so common that ATPG build them in for quick and easy use.

| Action | Grammar |
| :--- | ---: |
| `spc` | parses space: `< \t>` |
| `nl` | parses newline: `"\r\n"|"\r"` |
| `eol` | parses end-of-line: `nl|<end>` |