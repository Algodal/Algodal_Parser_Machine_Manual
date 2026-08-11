# Inbetween

The inbetween feature lets you specify actions that are parsed **cleanly** *in between* other actions. It is essentially a "skip" parse, similar to what you would write by hand in a hand-written parser. It is used with `.` inside the action grammar, and its config is defined with the same `.`.

```parser
stmt = "(" . "A" . ")"; # for every `.`, the list defined in the
# config of `.` is called repeatedly until no more parses are available.

. {
    spc
}
```

:::{important}
If you use `.` anywhere in your grammar, you **must** define the `.` config block that lists what to skip. See [Binding Power](binding_power.md) and [Samples](samples.md) for `.` used alongside a full parser.
:::

