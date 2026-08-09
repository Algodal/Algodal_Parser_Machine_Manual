# Inbetween

The inbetween function allows us to specify actions that must be parse **cleanly** *in between* other actions. It is essentially a "skip" parse similar to hand-written parsers. It is defined with `.` within the action grammar and its config is defined with the same `.`.

```
stmt = "(" . "A" . ")"; # for every `.` the list specified
# in the config of `.` is called repeatedly until no parse is available.

. {
    spc
}
```

