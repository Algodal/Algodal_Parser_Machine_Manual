# Counter

Counter is a feature that multiplies the same parse. It uses the symbols `+`, `*`, `?`, `-<number>` and `-<number>:<number` (range).

```parser
<A:Z>+;
```
The above is read "one or more A to Z".

| Count Operator Face | Description |
| :--- | ---: |
| `+` | one or more |
| `*` | zero or more |
| `<number>` | exactly `<number>` |
| `<number>`:`<number>` | atleast `<number>` up to `<number>` |

```parser
<A:Z>+;
<A:Z>*;
<A:Z>?;
<A:Z>-5;
<A:Z>-7:12;
```
