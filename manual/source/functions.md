# Functions

Actions allow some functions for additional parsing power.

| Result Operative Function | Description |
| :--- | ---: |
| `is`   | Compares the items with the parsed text for the first match |
| `not`  | Compares the items with the parsed text for no matches |
| `kind` | Compares the items with the parsed text for a sub-match |
| `tex`  | Returns the text that was parsed |
| `len`  | Returns the length of the text that was parsed |
| `to_num` | Converts parsed result a number 0 to max (negative and decimal numbers not supported) |

| Transformative Function | Description |
| :--- | ---: |
| `inbetween` | Insert parsing items *in between* parsing items to simply the latter |

| Directive Function | Description |
| :--- | ---: |
| `lookahead` | After parsing, reset the pointer to the original position |
| `order` | Parse the text as same length of the parameter string and match in any character order |
| `oneof` | Parse a single character and match any of the character of the string parameter |
| `char`  | Parse a single character |
| `<string>` | Parse the text as same length of the string and match exactly |

