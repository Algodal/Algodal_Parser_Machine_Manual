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

## Running several parsers together

When a grammar says `link javascript;`, its calls into that module are names
until the two are loaded side by side. Bring them together in a **link set**:
every binary joins it, the main one first, and a `javascript::stmt` anywhere in
the set resolves against it.

```c
#include "apm_vm.h"
#include "vm/link.h"
#include "io/read_binary_file.h"
#include "io/read_source_file.h"

int main(void)
{
    ApmVmLink*         set;
    ApmBinary          page, script;
    ApmVmConfig        config;
    ApmVmResult        result;
    ApmAllocatedBuffer text;
    uint32_t           length = 0, padded = 0;
    int                ok = 0;

    page   = ApmReadBinaryFile("html.apmb", &ok);
    script = ApmReadBinaryFile("javascript.apmb", &ok);
    text   = ApmReadSourceFile("page.html", &length, &padded);

    set = ApmVmLinkCreate();
    ApmVmLinkAddBinary(set, NULL, page);      /* index 0: the one that starts */
    ApmVmLinkAddBinary(set, NULL, script);

    config.input.ptr  = (char*)text;
    config.input.len  = length;
    config.padded_len = padded;

    result = ApmVmRunLinked(set, config);

    printf("consumed %u of %u bytes\n", result.bytes_length, length);

    ApmDestroyVmResult(result);
    ApmVmLinkDestroy(set);                    /* the set, then the binaries */
    ApmDestroyBinary(page);
    ApmDestroyBinary(script);
    ApmFreeAllocatedBuffer(text);
    return 0;
}
```

**The first binary added is the one the run starts from.** Order matters only
for that; the rest may be added in any order.

The set does not own what it is handed, so each binary is destroyed by whoever
loaded it, exactly as it would be without a link.

Each program keeps its own stack, its own globals and its own semvar sets. They
are run together, never merged.

From the command line the same thing is:

```sh
apmr html.apmb page.html --link javascript.apmb
```

Without the link, a call into the other module reports that it was never
resolved, rather than failing somewhere stranger.

## Parsers that do not know about each other

A link set is for parsers that **call** each other. Two unrelated parsers need
none of it: load each one and run it, because nothing about the VM is tied to
one grammar. They can be live at the same time, and in different threads, since
what differs between them is data rather than code.

:::{seealso}
How one module calls into another is described in [Module](module.md).
:::
