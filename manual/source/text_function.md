# Text Function

| Function | Description |
| :--- | ---: |
| `order` | Parse the text as same length of the parameter text and match in any character order |
| `oneof` | Parse a single character and match any of the character of the text parameter |
| `icase`  | Parse text with case insensitivity |



```
A = tex::order("ABC"); # similar to perm for syntactic objects
B = tex::oneof("ABC"); # a single character from the text
C = tex::icase("ABC"); # exact but with any case
```