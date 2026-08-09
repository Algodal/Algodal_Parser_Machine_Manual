# Parser Result Function

Once a parse occurs, it returns a result. That result can have additional processing act on it,

Actions allow some functions for additional parsing power.

| Result Operative Function | Description |
| :--- | ---: |
| `is`   | Compares the items with the parsed text for the first match |
| `not`  | Compares the items with the parsed text for no matches |
| `subkind` | Compares the items with the parsed text for a sub-match |
| `to_text`  | Returns the text that was parsed |
| `length`  | Returns the length of the text that was parsed |
| `to_number` | Converts parsed result a number 0 to max (negative and decimal numbers not supported) |
| `part` | Returns a sub-text of the parsed text |




```
name = <A:Za:z>+;
t1 = name::is("Fred"); # or name >> parval x x::is("Fred"); | checks if the result equals "Fred"
t2 = name::subkind("Fr"); # checks if result has substring called "Fr"
t3a = name::part(1); # section the result; returns first character; 1 index based
t3b = name::part(1:4); # section the result; returns first to fourth character
t3c = name::part(2+); # section the result; returns second to last character
t3d = name::part(1)::is(0x20); # chain functions
t3e = name::part(3:4)::is("ed"); # chain functions
t4a = name::not("Amber"); # checks that the result is not text "Amber"
t4b = char::not("A"); # your checks should be relative to the size
t4c = char::not(tex::oneof("hello")); # can pass text functions as parameters
t4d = char*::not("This"); # no difference with counters
```