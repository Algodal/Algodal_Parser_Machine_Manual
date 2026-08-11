# IF statement

The IF statement lets you branch the parsing based on a condition or on whether an action parses.

```parser
numval x = 0

A = char >> x; # auto-conversion to numval
B = C if({x == 1}) [T|F] D; # if logic is true then parse T else parse F
E = G if(M) [T | F]; # if M parses, then parse T else parse F
H = I if(M) [T];  # if M parses, then parse T
J = K if(M) [|F]; # if M fails to parse then parse F
```