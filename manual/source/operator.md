# Operator

The operate can influence the unit of an action. There is one (so far) - the count operator.

## Count Operator

The count operator is defined with *[]* brackets. The *()* for parameters is optional.

```parser
[+] oneof "ABCDE";
```
The above is read "one or more of one of A-B-C-D or E".

| Count Operator Face | Description |
| :--- | ---: |
| `+` | one or more |
| `*` | zero or more |
| `<number>` | exactly `<number>` |
| `<number>`:`<number>` | atleast `<number>` up to `<number>` |

```parser
[+] oneof "ABCDE";
[*] oneof "ABCDE";
[5] oneof "ABCDE";
[7:12] oneof "ABCDE";
```

## Regex-like Syntax

The standard syntax go from left to right and affect parameters on the right.However, the count operator has a short cut form that resemble **regex**. This form is from right to left and affect the parameter on the left. The slight difference is the <number> formats which is lead by `-`.

```parser
(oneof "ABCDE")+;
(oneof "ABCDE")*;
(oneof "ABCDE")-5;
(oneof "ABCDE")-7:12;
```