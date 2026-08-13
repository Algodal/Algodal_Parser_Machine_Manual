# Syntax highlighter for the Algodal Parser Machine Language (APML).
#
# This module defines a Pygments lexer for APML and registers it under the
# alias ``parser`` so that fenced code blocks written as ```` ```parser ````
# are highlighted throughout the manual.
#
# It is imported and registered by ``conf.py`` via ``app.add_lexer``.

from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)


class ParserLexer(RegexLexer):
    """Pygments lexer for the Algodal Parser Machine Language (APML)."""

    name = "APML"
    aliases = ["parser", "apml"]
    filenames = ["*.apml"]

    # Block / command keywords that open a grammar construct.
    _KEYWORDS = (
        "program",
        "link",
        "parser",
        "config",
        "bindpow",
        "custom_action",
        "alias",
        "perm",
        "if",
    )

    # Variable type keywords.
    _TYPES = (
        "parval",
        "texval",
        "numval",
        "semval",
    )

    # Built-in actions provided by the machine.
    _BUILTINS = (
        "spc",
        "nl",
        "eol",
        "char",
    )

    # Namespace / result functions invoked after ``::`` (or the ``tex`` namespace).
    _FUNCTIONS = (
        "order",
        "oneof",
        "icase",
        "is",
        "not",
        "subkind",
        "part",
        "to_text",
        "to_number",
        "length",
        "count",
    )

    tokens = {
        "root": [
            (r"\s+", Whitespace),
            # Line comments — always to end of line.
            (r"#.*$", Comment.Single),
            # Strings.
            (r'"', String, "string"),
            # Character literals — \x.. hex and \u.. unicode. Chains (,) and
            # ranges (:) are part of the same literal, so they take the same
            # color as a single literal (e.g. \x43,41,54 and \x41:5A).
            (r"\\[xu][0-9A-Fa-f]+(?:[,:][0-9A-Fa-f]+)*", String.Escape),
            # Regex / character blocks — any content between < and >.
            (r"<[^>\n]*>", String.Regex),
            # Namespace before ::  (e.g. tex::oneof)
            (r"\b(tex)(::)", bygroups(Name.Namespace, Operator)),
            # Result / namespace functions after ::  (e.g. name::is, a::to_text)
            (r"(::)(" + "|".join(_FUNCTIONS) + r")\b",
             bygroups(Operator, Name.Function)),
            # Numeric literals (decimal only — 0 or positive).
            (r"\d+", Number.Integer),
            # Config keys and enum values — a leading dot followed by a name.
            (r"\.[a-zA-Z_]\w*", Name.Attribute),
            # Keywords, types, builtins.
            (words(_KEYWORDS, suffix=r"\b"), Keyword),
            (words(_TYPES, suffix=r"\b"), Keyword.Type),
            (words(_BUILTINS, suffix=r"\b"), Name.Builtin),
            # Identifiers (actions, variables).
            (r"[a-zA-Z_]\w*", Name),
            # Operators — longest first.
            (r":=|->|>>|::", Operator),
            (r"[=|/+*?:.\-!]", Operator),
            # Punctuation.
            (r"[\[\](){},;]", Punctuation),
            # Catch-all.
            (r".", Name),
        ],
        "string": [
            (r'"', String, "#pop"),
            (r"\\.", String.Escape),
            (r'[^"\\]+', String),
        ],
    }


def setup(app):
    app.add_lexer("parser", ParserLexer)
    app.add_lexer("apml", ParserLexer)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
