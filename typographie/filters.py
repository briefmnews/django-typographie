import re
import html


from .registry import register_filter
from .smartypants import smartyPants


non_break = "\xa0"
french_characters = "A-Za-z0-9àâéèêëîïôöùûüçœ€°ÀÂÉÈÊËÎÏÔÖÙÛÜÇŒ"

# percent 9% and 9 %
re_percent = re.compile(r"([0-9])\s*(%)", flags=re.U)
re_percent_with_comma = re.compile(r"([0-9]+)\s*,\s*([0-9]+)\s*(%)", flags=re.U)
re_digit = re.compile(r"([0-9])\s", flags=re.U)

re_opening_quote = re.compile('\xab([{}“"])'.format(french_characters))
re_closing_quote = re.compile("([{},\.…!?;%'’\(\)”\"])\xbb".format(french_characters))
re_briefme = re.compile("(\sbrief\.me)", flags=re.IGNORECASE)


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
    text = re_percent_with_comma.sub("\\1,\\2\xa0\\3", text)

    text = re_digit.sub("\\1\xa0", text)
    text = re_briefme.sub(
        '<a href="http://brief.me" style="color: #4a4a4a;'
        ' text-decoration: none; cursor: default;">\\1</a>',
        text,
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
    # let's remove the nbsp before
    text = text.replace("&nbsp;", "")
    text = text.replace(non_break, " ")

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


@register_filter
def exponent(text):
    """To manage exponent"""
    text = force_text(text)
    text = re.sub("(^|\s)([1I])(er)(\s|\.|,|$)", "\\1\\2<sup>\\3</sup>\\4", text)
    text = re.sub("(^|\s)([1-9]\d{0,2})(e)(\s|\.|,|$)", "\\1\\2<sup>\\3</sup>\\4", text)
    text = re.sub(
        "(^|\s)(X{0,3}(IX|IV|V?I{0,3}))(e)(\s|\.|,|$)", "\\1\\2<sup>\\4</sup>\\5", text
    )

    return text


re_indice = [
    re.compile("(^|\s)(CO)(2)(\s|\.|,|$)"),
]


@register_filter
def indice(text):
    """Manage indice"""
    text = force_text(text)
    for regex in re_indice:
        text = regex.sub("\\1\\2<sub>\\3</sub>\\4", text)
    return text


@register_filter
def metric(text):
    text = re.sub("(\s)(m|km)([23])(\s|\.|,|$)", "\\1\\2<sup>\\3</sup>\\4", text)

    return text
