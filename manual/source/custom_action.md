# Custom Action

```parser
name = <A:Za:z> (<A:Za:z_0:9>)*;
structure1 := name . ":" . indent (name newline)* dedent;
structure2 := name special_tab name;

# placeholder definition of actions (REQUIRED!)
indent = _; # indicates that the action grammar is defined externally through user customized code.
dedent = _;
special_tab = _;
newline = _;

# Reference linking of the custom action with user code. Actual linking is done outside DSL.
# User code is called on text where ever action is used to generate syntactic objects.
custom_action { 
    indent: "apm_py_indent",
    dedent: "apm_py_dedent",
    newline: "apm_py_newline",
    special_tab: "myfunc"
}
```