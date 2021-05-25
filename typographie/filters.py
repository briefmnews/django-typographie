import re
import html


from .registry import register_filter
from .smartypants import smartyPants


non_break = "\xa0"
french_characters = "A-Za-z0-9àâéèêëîïôöùûüçœ€°ÀÂÉÈÊËÎÏÔÖÙÛÜÇŒ"

# percent 9% and 9 %
re_percent = re.compile(r"([0-9])\s*(%)", flags=re.U)
re_percent_with_comma = re.compile(
    r"(^|\s)([0-9]\d{0,2})\s*,\s*([0-9]+)\s*(%)", flags=re.U
)
re_digit = re.compile(r"([0-9])\s", flags=re.U)

re_opening_quote = re.compile(r'\xab([{}“"])'.format(french_characters))
re_closing_quote = re.compile(r"([{},\.…!?;%'’\(\)”\"])\xbb".format(french_characters))
re_prevent_underline = [
    (
        re.compile(r"brief\.me", flags=re.IGNORECASE),
        "B&zwnj;r&zwnj;i&zwnj;e&zwnj;f&zwnj;.&zwnj;m&zwnj;e",
    ),
    (re.compile(r"slate\.fr", flags=re.IGNORECASE), "Slate&zwnj;.&zwnj;fr"),
    (re.compile(r"slate\.com", flags=re.IGNORECASE), "Slate&zwnj;.&zwnj;com"),
    (
        re.compile(r"vie-publique\.fr", flags=re.IGNORECASE),
        "Vie-publique&zwnj;.&zwnj;fr",
    ),
    (
        re.compile(r"service-public\.fr", flags=re.IGNORECASE),
        "Service-public&zwnj;.&zwnj;fr",
    ),
    (re.compile(r"arte\.tv", flags=re.IGNORECASE), "Arte&zwnj;.&zwnj;tv"),
]
re_exponent = [
    (re.compile(r"(^|\s)([1I])(er)(\s)"), "\\1\\2<sup>\\3</sup>\xa0"),
    (re.compile(r"(^|\s)([1I])(er)(\.|,|$)"), "\\1\\2<sup>\\3</sup>\\4"),
    (re.compile(r"(^|\s)([1-9]\d{0,2})(e)(\.|,|$)"), "\\1\\2<sup>\\3</sup>\\4"),
    (re.compile(r"(^|\s)([1-9]\d{0,2})(e)(\s)"), "\\1\\2<sup>\\3</sup>\xa0"),
    (re.compile(r"(^|\s)([XIV]{1,5})(e)(\.|,|$)"), "\\1\\2<sup>\\3</sup>\\4"),
    (re.compile(r"(^|\s)([XIV]{1,5})(e)(\s)"), "\\1\\2<sup>\\3</sup>\xa0"),
]
specific_words = [
    r"(CAC)(\s)(40)",
    r"(Europe)(\s)(1)",
    r"(SBF)(\s)(120)",
    r"(France)(\s)(24)",
    r"(Système)(\s)(U)",
    r"(Hyper)(\s)(U)",
    r"(Super)(\s)(U)",
    r"(France)(\s)(2)",
    r"(France)(\s)(3)",
    r"(France)(\s)(4)",
    r"(France)(\s)(5)",
    r"(France)(\s)(24)",
    r"(Napoléon)(\s)(I<sup>er</sup>)",
    r"(Napoléon)(\s)([XIV]{1,5})",
    r"(Louis)(\s)(I<sup>er</sup>)",
    r"(Louis)(\s)([XIV]{1,5})",
    r"(Jean-Paul)(\s)(I<sup>er</sup>)",
    r"(Jean-Paul)(\s)([XIV]{1,5})",
    r"(Benoît)(\s)(I<sup>er</sup>)",
    r"(Benoît)(\s)([XIV]{1,5})",
    r"(Paul)(\s)(I<sup>er</sup>)",
    r"(Paul)(\s)([XIV]{1,5})",
    r"(Jean)(\s)(I<sup>er</sup>)",
    r"(Jean)(\s)([XIV]{1,5})",
    r"(Pie)(\s)(I<sup>er</sup>)",
    r"(Pie)(\s)([XIV]{1,5})",
]
re_subscript = [
    re.compile(r"(^|\s|\()(CO)(2)(\s|\.|,|<|\)|$)"),
]
re_metric = [
    (re.compile(r"(^|\s)(m|km)([23])(\)|\.|,|$)"), "\\1\\2<sup>\\3</sup>\\4"),
    (re.compile(r"(^|\s)(m|km)([23])(\s)"), "\\1\\2<sup>\\3</sup>\xa0"),
]


def cb_re_content_between_tags(matchobj):
    text = matchobj.group(2)

    # non break space before double punctuation
    for c in ":;!?":
        text = text.replace(" {}".format(c), "{}{}".format(non_break, c))

    # remove non break space after opening and before closing
    text = text.replace("\xab ", "\xab")
    text = text.replace(" \xbb", "\xbb")

    # non break space for opening and closing quotes
    text = re_opening_quote.sub("\xab\u00a0\\1", text)
    text = re_closing_quote.sub("\\1\u00a0\xbb", text)

    # replace any white space between an integer and % and replace it with \xa0
    text = re_percent.sub("\\1\xa0\\2", text)
    text = re_percent_with_comma.sub("\\1\\2,\\3\xa0\\4", text)

    text = re_digit.sub("\\1\xa0", text)

    # Handle prevent underline exceptions
    for regex, replace in re_prevent_underline:
        text = regex.sub(replace, text)

    # Handle exponents for roman / arabic numerals
    for regex, replace in re_exponent:
        text = regex.sub(replace, text)

    # Handle subscript
    for regex in re_subscript:
        text = regex.sub("\\1\\2<sub>\\3</sub>\\4", text)

    # Handle metric
    for regex, replace in re_metric:
        text = regex.sub(replace, text)

    # Handle word with non breaking space
    for word in specific_words:
        text = re.compile(r"(^|\s){word}".format(word=word)).sub("\\1\\2\xa0\\4", text)
        text = re.compile(r"(^|\s){word}(\xa0)".format(word=word)).sub(
            "\\1\\2\xa0\\4 ", text
        )

    return "%s%s%s" % (matchobj.group(1), text, matchobj.group(3))


# extract html between tags div, p, pre, blockquote
re_parse_content = re.compile(
    r"(.*?<[^>]* ?)((?:div|p|pre|blockquote|h[1-6]))( ?[^>]*>)(.*?)(</\2>.*?)",
    flags=re.S + re.U,
)


def cb_re_parse_content(matchobj):
    text = spaces(matchobj.group(4))
    return "%s%s%s%s%s" % (
        matchobj.group(1),
        matchobj.group(2),
        matchobj.group(3),
        text,
        matchobj.group(5),
    )


# extract content between two tags
re_content_between_tags = re.compile(r"(>|^)([^<>]*)(<|$)")


@register_filter
def unescape(text):
    return html.unescape(text)


@register_filter
def force_text(text):
    from django.utils.encoding import force_text as django_force_text

    return django_force_text(text)


@register_filter
def smartypants(text):
    return smartyPants(text)


@register_filter
def ellipsis(text):
    text = re.sub(r"\.\.\.", "\u2026", text)
    text = re.sub(r"\. \. \.", "\u2026", text)

    return text


@register_filter
def spaces(text):
    text = text.strip()
    if re_parse_content.match(text) is not None:
        text = re_parse_content.sub(cb_re_parse_content, text)
    else:
        # set spaces
        text = re_content_between_tags.sub(cb_re_content_between_tags, text)
    return text


widont_finder = re.compile(
    r"""((?:</?(?:a|em|span|strong|i|b)[^>]*>)|[^<>\s])
                                   \s+
                                   ([^<>\s]+
                                   \s*
                                   (</(a|em|span|strong|i|b)>\s*)*
                                   ((</(p|h[1-6]|li|dt|dd)>)|$))
                                   """,
    re.VERBOSE,
)


def widont(text):
    text = widont_finder.sub("\\1\xa0\\2", text)
    return text
