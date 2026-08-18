# Built-in Action

Some actions are so common that APM builds them in for quick and easy use.

| Action | Grammar |
| :--- | ---: |
| `spc` | parses space |
| `nl` | parses newline |
| `eol` | parses end-of-line |

## The equivalent to the built-in actions

```parser
spc = < \t>;
nl = "\r\n" \ <\n>;
eol = nl \ <apm:no_more_incoming_text>; # APM provided signal
```