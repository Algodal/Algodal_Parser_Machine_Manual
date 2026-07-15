# Action

A grammar action (or simply action) is the definition of a parsing action. It can be a character parser or a token parser or both. The type the action is resolved as is determined by the generator at compile time (the process of generation) and based on the output structure defined by the user.

In below example, we defined an action called animal and it parses for an exact match for the string *"cat"*.

```parser
animal = "cat"
```

In the next example, we defined 3 actions: dog parsers for exactly "dog", cat parses for exactly "cat" and animal parses for actions *dog* followed by *cat* which is equivalent to *`animal = "dog" "cat"`*.

```parser
dog = "dog"
cat = "cat"
animal = dog cat
```

In this example, it is similar to the previous example except that animal parses for the action *dog* *OR* the action *cat*.

```parser
dog = "dog"
cat = "cat"
animal = dog | cat
```

This example is the same except animal parses for the action *dog* *OR* the action *cat* *whichever first*.

```parser
dog = "dog"
cat = "cat"
animal = dog / cat
```

The difference between the last 2 examples is `|` *OR* and `/` *Firstly OR*. In the case of *OR* all cases are checked regardless of any being successful. While in the case of *Firstly OR* all checks stop on the *first* successful case. So in the example `animal = dog | cat`, even if dog successfully parses the text, the parser will still check if cat parses. While in the case of `animal = dog / cat`, cat will only be checked if dog failed to parse.

An action can be considered to be containing *series* and *options*.

```parser
act = A B C
```

`A B C` are actions that are parsed in that order: A followed by B followed by C. This is called a *series*. Each member of a series is generally called a *unit*.

```parser
act = D | E
```

`D | E` are actions that are parsed in *parallel*. This is called an *option*. Even if the parser goes through all *options* only one *option* can be *move* the parsing progress. If we had `D / E` instead (also an option), we stop checking other possible options once we find the first successful parse.

```parser
act = A B C | D 
```

Options are lists of series. Therefore in the case `A B C | D` the parser will see an *option* of series `A B C` *OR* series `D`.

```parser
act = A B C | D E | F G H
```

So `A B C | D E | F G H` is an option of 3 series: `A B C` *OR* `D E` *OR* `F G H`.

If we wanted to change how the parser interpret the series and options we can use *groups*. Groups can be defined anywhere and it is defined using curved-brackets `()`.

```parser
act = A B (C | D) E | F G H
```

Because of the group `(C | D)`, at the level of `act` action we have an option of 2 series. `(C | D)` is interpret as a *unit* in the series `A B (C | D) E`. The second series is `F G H`. If we zoom in into the unit `(C | D)` it is a group of an option of 2 series `C` and `D`.

A group can go anywhere:

```parser
act = (A B (C | D) E | F (G) H)
```
