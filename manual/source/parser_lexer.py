# Syntax highlighter for the Algodal Parser Machine Language (APML).
#
# This module defines a Pygments lexer for APML and registers it under the
# alias ``parser`` so that fenced code blocks written as ```` ```parser ````
# are highlighted throughout the manual.
#
# It is imported and registered by ``conf.py`` via ``app.add_lexer``.
#
# The word lists below are the language's RESERVED WORDS, and they are meant to
# match what the manual's Keywords chapter prints. Adding a keyword to the
# language means adding it here too, or it is coloured as an ordinary
# identifier.

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
    filenames = ["*.apm", "*.apml"]

    # Declarations and control: the words that open a construct.
    _KEYWORDS = (
        "program",
        "link",
        "parser",
        "config",
        "feat",
        "bindpow",
        "foreign",
        "node_id",
        "alias",
        "perm",
        "give",
        "if",
        "node",
    )

    # Variable, set and scope declarations.
    _TYPES = (
        "texvar",
        "numvar",
        "semvar",
        "scope",
    )

    # Provided by the machine: the matchers and the system function.
    _BUILTINS = (
        "spc",
        "nl",
        "eol",
        "eof",
        "char",
        "error",
    )

    # Called after ``::`` -- result functions, semvar and scope calls.
    _FUNCTIONS = (
        "order",
        "oneof",
        "icase",
        "is",
        "not",
        "subkind",
        "part",
        "char_count",
        "to_num",
        "iter_steps",
        "first",
        "begin",
        "end",
        "clear",
    )

    # Logic operators are words, and so are the two config values.
    _LOGIC = ("AND", "OR", "NOT")
    _VALUES = ("TRUE", "FALSE")

    tokens = {
        "root": [
            (r"\s+", Whitespace),
            # Line comments -- always to end of line.
            (r"#.*$", Comment.Single),
            # Strings.
            (r'"', String, "string"),
            # Character literals -- \x.. hex and \u.. code point. Chains (,)
            # and ranges (:) belong to the same literal, so they take the same
            # colour (e.g. \x43,41,54 and \x41:5A).
            (r"\\[xu][0-9A-Fa-f]+(?:[,:][0-9A-Fa-f]+)*", String.Escape),
            # Any other escaped character.
            (r"\\.", String.Escape),
            # Character blocks -- a set of characters between < and >.
            (r"<[^>\n]*>", String.Regex),
            # An astmap label: 'name', written against the unit it names.
            (r"'[A-Za-z0-9_]+'", Name.Label),
            # The tex namespace before ::  (e.g. tex::oneof)
            (r"\b(tex)(::)", bygroups(Name.Namespace, Operator)),
            # A call after ::  (e.g. name::is, kind::first, blk::begin)
            (r"(::)(" + "|".join(_FUNCTIONS) + r")\b",
             bygroups(Operator, Name.Function)),
            # Binding to a precedence table at the call site: bp::-expr
            (r"(::)(-)([A-Za-z_]\w*)",
             bygroups(Operator, Operator, Name.Function)),
            # Numeric literals (decimal only -- 0 or positive).
            (r"\d+", Number.Integer),
            # Logic operators and config values, before plain identifiers.
            (words(_LOGIC, suffix=r"\b"), Operator.Word),
            (words(_VALUES, suffix=r"\b"), Keyword.Constant),
            # Keywords, types, builtins.
            (words(_KEYWORDS, suffix=r"\b"), Keyword),
            (words(_TYPES, suffix=r"\b"), Keyword.Type),
            (words(_BUILTINS, suffix=r"\b"), Name.Builtin),
            # A bodiless action, bound to the host's C: `indent = _;`
            (r"(?<![A-Za-z0-9_])_(?![A-Za-z0-9_])", Name.Builtin.Pseudo),
            # Identifiers (actions, variables).
            (r"[a-zA-Z_]\w*", Name),
            # Operators -- longest first, so := is not read as : then =.
            (r":=|->|=>|::", Operator),
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
