# How to Use

A grammar is only half of a parser. The other half is the VM, which you build
into your own program once and then point at whatever parser program you like.

This page is a sketch, not a build recipe. The code below is here to show the
shape of the thing.

## The two pieces

```
grammar.apm  ──apma──▶  grammar.apmb  ──▶  the VM in your program  ──▶  an AST
```

`apma` is the compiler. It turns your grammar into a parser program, a file.
The VM is C that you compile into your project. Because the VM is the same for
every grammar, you integrate it once.

## Compiling a grammar

```sh
apma mylang.apm -o mylang.apmb
```

## Running it

```c
#include "apm_vm.h"
#include "io/read_binary_file.h"
#include "io/read_source_file.h"
#include "api/apm_nav.h"

int main(void)
{
    ApmBinary          program;
    ApmVmConfig        config;
    ApmVmResult        result;
    ApmAllocatedBuffer text;
    uint32_t           length = 0, padded = 0;
    int                ok = 0;

    /* the parser program */
    program = ApmReadBinaryFile("mylang.apmb", &ok);
    if (!ok) return 1;

    /* the text to parse */
    text = ApmReadSourceFile("input.txt", &length, &padded);

    config.input.ptr  = (char*)text;
    config.input.len  = length;
    config.padded_len = padded;

    result = ApmVmRun(program, config);

    printf("consumed %u of %u bytes, %u root nodes\n",
           result.bytes_length, length, result.count);

    ApmDestroyVmResult(result);
    ApmFreeAllocatedBuffer(text);
    ApmDestroyBinary(program);
    return 0;
}
```

## Reading the tree

`result.nodes` holds the root nodes, in the order they were parsed, and
`result.count` says how many. Each node carries a name and a span of the input:

```c
for (uint32_t i = 0; i < result.count; i++)
{
    uint32_t    n = 0, v = 0;
    const char* name  = ApmNodeNameOf(program, result.nodes[i], &n);
    ApmReadOnlyBuffer value = ApmGetNodeValue(result.nodes[i], (char*)text, &v);

    printf("%.*s = %.*s\n", (int)n, name, (int)v, (const char*)value);
}
```

A node's value is a **span of the input**, not a copy, which is why the text
buffer has to outlive the tree.

## Several parsers at once

Nothing about the VM is tied to one grammar, so loading a second parser program
is the same three lines again. Two parsers can be live in one program, and in
different threads, because what differs between them is data rather than code.

:::{seealso}
To have one parser call into another, see [Module](module.md).
:::
