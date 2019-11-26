# encoding: utf-8
from typographie.templatetags.typographie import spaces, _typographie
from typographie.templatetags.smartypants import smartyPants


class TestTypographieSpaces(object):
    def test_div(self):
        text = "<div>un test : test</div>"
        assert spaces(text) == "<div>un test\xa0: test</div>"

    def test_column(self):
        text = "un test : test"
        assert spaces(text) == "un test\xa0: test"

    def test_column_with_tags(self):
        text = '<a href="">un test</a> : test'
        assert spaces(text) == '<a href="">un test</a>\xa0: test'

    def test_semi_column(self):
        text = "un test ; test"
        assert spaces(text) == "un test\xa0; test"

    def test_semi_column_with_tags(self):
        text = '<a href="">un test</a> ; test'
        assert spaces(text) == '<a href="">un test</a>\xa0; test'

    def test_exclamation_mark(self):
        text = "un test ! test"
        assert spaces(text) == "un test\xa0! test"

    def test_exclamation_mark_with_tags(self):
        text = '<a href="">un test</a> ! test'
        assert spaces(text) == '<a href="">un test</a>\xa0! test'

    def test_interrogation_mark(self):
        text = "un test ! test"
        assert spaces(text) == "un test\xa0! test"

    def test_interrogation_mark_with_tags(self):
        text = '<a href="">un test</a> ? test'
        assert spaces(text) == '<a href="">un test</a>\xa0? test'

    def test_closing_quotation_mark_with_period(self):
        text = "test\xbb."
        assert spaces(text) == "test\xa0\xbb."

    def test_quotation_mark_with_quote(self):
        text = "\xabactualité\xbb</a>."
        assert spaces(text) == "\xab\xa0actualité\xa0\xbb</a>."

    def test_with_quote(self):
        text = "<strong>\xabtest\xbb</strong>."
        assert spaces(text) == "<strong>\xab\xa0test\xa0\xbb</strong>."

    def test_nonbreakable_after_digit(self):
        text = "10 personnes"
        assert spaces(text) == "10\xa0personnes"

    def test_nonbreakable_between_digits(self):
        text = "10 000"
        assert spaces(text) == "10\xa0000"

    def test_nonbreakable_between_digit_percent(self):
        text = "10%"
        assert spaces(text) == "10\xa0%"
        text = "10 %"
        assert spaces(text) == "10\xa0%"

    def test_briefme(self):
        text = "Today in brief.me we talk about"
        assert (
            spaces(text) == 'Today in <a href="http://brief.me"'
            ' style="color: #4a4a4a; text-decoration: none; cursor:'
            ' default;">brief.me</a> we talk about'
        )

    def test_exponent(self):
        text = "1<sup>er</sup> to see"
        assert _typographie(text) == "1<sup>er</sup>\u00a0to see"

        other_text = "I<sup>er</sup> to see"
        assert _typographie(other_text) == "I<sup>er</sup>\u00a0to see"

    def test_ampersand(self):
        text = "To test with an ampersand h&m for example"

        assert _typographie(text) == "To test with an ampersand h&m for example"


class TestTypographieSmartyPants(object):
    def test_replace_quotes(self):
        text = '"test"'
        assert smartyPants(text) == "\xabtest\xbb"
