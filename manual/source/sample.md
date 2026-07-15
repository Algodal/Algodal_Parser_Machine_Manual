# Sample

**INI Parser**

```parser
lexer {
  (comment \ newline \ space)+;
  "[" space* heading space* "]";
  key space* "=" space* value;
} :: token {
  newline {~discard},
  heading,
  key,
  value
}

key = identifier;
value = char::not(newline, ";", eof);
heading = identifier;
comment = ";" char::not(newline, eof);
newline = ("\r\n" | "\n");
identifier = $<A-Z>+;
space = < \t>+; 

analyzer {
  section;
  stmt;
} :: syntax {...}

section = heading (newline stmt)*
stmt = key value
```

**Symantic Predicates**

```parser
# Semantic Predicates

tabval user_types;
scope {
  ("{", "}") : {user_types}
}

custom_type = indentifier -> user_types
parse_something = user_types

identifier = $<A-Z>+;
type = builtin_type | user_types;
builtin_type = "int"

value = identifier
identifier = <A-Z>+
content = identifier


lexer {
  "{"; "}";
  ("typedef" type custom_type ";")::inbetween(space, newline);
  type;
} :: token {
  "{", "}", type, var
}
```